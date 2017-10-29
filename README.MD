#Projekt IIS - IS pro e-sport#

##Zadání##
Vytvořte informační systém pro profesionální hráče e-sportu (elektronický sport) a správu turnajů a zápasů. Hráči, mimo své reálné jména, mají své přezdívky a evidují svoje vybavení (herní myši, klávesnice, grafiky, apod.) a zaměřují se na specifické hry. Hráči se dále seskupují do klanů, které jsou zaměřené na specifickou hru, nebo se může jednat o multi-herní komunity. Klany jsou jak mezinárodní nebo specifické pro jednu zemi, mají své loga, hymny a vůdce klanů. Systém umožňuje klanům hledat nové hráče podle her, na které se specializují i podle předchozích výsledků v turnajích. Systém dále umožňuje hráčům procházet hry, jejich data vydaní, herní žánry, herní módy (např. 5 vs 5, 1 vs 1, …), vydavatele apod. Pro účely kompetivnosti se vytváří týmy, různých velikostí se specifickými jmény, přičemž týmy mohou být meziklanové nebo čistě v rámci klanů. Týmy se pak dále účastní buď velkých turnajů, které jsou financovány společnostmi, anebo pouze přátelských zápasů či tréninků (tzv. scrim). U každého turnaje evidujeme výsledky jednotlivých zápasů, výherce turnajů, ale i hlavní a vedlejší sponzory, hlavní cenu a hra (nebo hry), které se v rámci turnaje hrály. Systém navíc umožňuje tisknout statistiky hráčů, jak v rámci jednotlivých her, tak proběhlých turnajích či v rámci klanu. Speciální možností systému je pak navíc možnost zapsat se na odběr informací o chystaných turnajích.

##Pracovní výcuc##
###Login###
- User (player)
- Worker (asi ne)
- Admin

###Podstránky###
- Player detail page
	- nickname
	- real name
	- specialized
	- clan (leader)
	- team (leader)
	- equipment list (solo multi column table)
- Team detail page
	- name
	- logo
	- desc
	- leader
	- members
	- zapasy
	- vyhrane turnaje
- Clan detail page
	- name
	- leader
	- song
	- logo
	- specialized
- Turnaj detail page icluding Match list
	- nazev
	- odemna 
	- sponzor
	- kdy
	- kde
	- capacity
	- type
		- common - winner
		- WC - winner, second, ..., fifth
- Match detail page
	- kdy 
	- score 
	- typ 
	- souper / souper
	- hra
	- turnaj?
- Game detail page
	- nazev
	- vydavatel 
	- rok vydani
	- zanr
	- mod
- Game list
	- prochazeni her jak na twitchi
- Player browser
	- prochazeni alb v itunes
- Clan Browser
	- prochazeni alb v itunes
- Team browser
	- prochazeni alb v itunes
- Printing stats

##Fungování##
- Neprihlasenemu uzivateli nabidnout pouze index s loginem 
