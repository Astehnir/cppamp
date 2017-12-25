import argparse
import pandas as pd
import calendar

# Ustawienia parametrów wywołania
parser = argparse.ArgumentParser(description= 'Robi jakieś excelowe shenanigans. I raportuje raptorami.')
parser.add_argument('-p', '--pickfile', required = True, help = 'Pozwala na tworzenie raportu z konkretnego pliku.')
parser.add_argument('-q', '--quiet', action = 'store_true', help = 'Wyświetla podsumowanie bez wypuszczania raptora.')
parser.add_argument('-u', '--unit', help = 'Pokazuje statystyki dla konkretnej osoby (bez raportowania).')

args = parser.parse_args()
plik = args.pickfile

suma_wplat = 0
srednia_wplata = 0
Fandoszlachta = []
Fandoplebs = []
szukany = None

# Wczytuje plik csv w kodowaniu ANSII albo UTF-8, przerabia kolumne 'Data' na nazwy miesięcy
# Sortuje całość tabeli alfabetycznie i grupuje
df_in = pd.read_csv(plik, encoding='ANSI' or 'UTF-8', parse_dates = ['Data'])
df_in['Data'] = pd.DatetimeIndex(df_in['Data']).month
df_in['Data'] = df_in['Data'].apply(lambda x: calendar.month_abbr[x])
df_in['Data'].to_string(header='Data')
df_in = df_in.sort_values(by=['Nick'], ascending=True)
df_in = df_in.groupby(['Nick', 'Data'], as_index=False).sum()

# Przerabia dataFrame na listę list, w której zdrowo mieszamy
listy = df_in.values.tolist()
for i in range(0, len(listy)-1):
    if listy[i][0] == listy[i+1][0]:
        listy[i][1] = listy[i][1] + (', ') + listy[i+1][1]
        listy[i][2] = listy[i][2] + listy[i+1][2]
        listy.pop(i+1)
    suma_wplat = suma_wplat + listy[i][2]

srednia_wplata = suma_wplat / len(listy)

# Sprawdza czy wpłata jest większa od średniej i przyporządkowuje odpowieni tytuł do późniejszego raportu
for i in range(0, len(listy)):
    if listy[i][2] < srednia_wplata:
        listy[i].append('Fandoplebs')
    else:
        listy[i].append('Fandoszlachta')

# To samo, tylko info idzie na ekran
for i in range(0, len(listy)):
    if listy[i][2] > srednia_wplata:
        Fandoszlachta.append(listy[i][0])
    else:
        Fandoplebs.append(listy[i][0])

# Info do wyświetlenia na ekran
if args.unit == None:
    print('Wpłaty sięgają milionów! A dokładnie: %.2fzł' %suma_wplat)
    print('Średnia wysokość wpłaty: %.2fzł' % srednia_wplata)
    print("Szlachta fandomanzy: ", Fandoszlachta)
    print("Plebs fandomanzy: ", Fandoplebs)
else:
    for i in range(0, len(listy)):
        if listy[i][0] == args.unit:
            print(listy[i])
            szukany = args.unit
        else:
            continue
    if szukany is not args.unit:
        print('Nie znam typa.')

# Wypluwa ładny raport, jeśli parametrysię zgadzają
if args.quiet == False and args.unit == None:
    raport = pd.DataFrame(listy, columns=['Nick','Miesiąc(e) wpłat(y)','Kwota wpłacona','Status'])
    raport.to_csv('raptor.csv', index=False)
    
