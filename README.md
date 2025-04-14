# Dogsteska

Dogsteska je projekt zaměřený na vývoj autonomního systému pro navigaci psa v prostoru, detekci překážek a skenování lístků pomocí kamery. Tento projekt je vyvíjen na modelu Unitree Go2¨

![Dogstestka](images/Picture1.png)

## Funkcionality

### 1. Chůze
Pes je schopen dojít na zadané souřadnice, které mu určíme.

### 2. Skenování lístků
- Kamera naskenuje objekty před sebou.
- Pokud se jedná o čárový kód, vrátí jeho číselnou hodnotu.

### 3. Detekce překážek
- Identifikace objektů, které se nacházejí v cestě psa.
- Reakce na překážky a úprava trasy.

### 4. Mapování prostoru
- Použití statické mapy s předdefinovanými body, kam se má pes dostat.
- Body jsou označeny čísly pro snadnější navigaci.

### 5. Testování
- Ověření funkcionality navigace, skenování a detekce překážek.
- Simulace různých scénářů pohybu psa.

## Instalace a spuštění

1. Klonuj tento repozitář:

```
git clone https://github.com/uzivatel/dogsteska.git
```

2. Přejdi do složky projektu:

```
cd dogsteska
```

3. Instaluj potřebné závislosti (pokud jsou vyžadovány):

```
pip install -r requirements.txt
```

4. Spusť hlavní skript:

```
python main.py
```

## Technologie
- Python
- OpenCV (pro skenování lístků)
- Unitree Go2 (hardware pro testování)
