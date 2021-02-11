<img src="sinkaf/data/sinkaf.png" width="120" />

> _"Kötü söz sahibine aittir."_
>
> -Anonim


## Nedir?

`sinkaf` uygunsuz yorumların bulunmasını sağlayan bir python kütüphanesidir.

## Farkı nedir?

Diğer algoritmalardan en büyük farkı, önceden belirlenmiş bir kelime listesinden cümlerlerdeki sözcükleri tek tek kontrol etmek yerine, makine öğrenmesi metodları kullanarak cümlenin genel anlamına bakabilmesidir. Aynı zamanda `sinkaf` baya bi hızlı! 

## Nasıl çalışıyor?

Arka planda modelimizi eğitmek için [A corpus of Turkish offensive language](https://coltekin.github.io/offensive-turkish/guidelines.html) verisetini kullanıyoruz. Bu veriseti 36,000+ twitter yorumunun hakaret içerip içermediğini gösteren, Türkçe ile makine öğrenmesi denemeleri yapmak isteyenler için fevkaledenin fevkinde bir kaynak! Kendilerine teşekkür ediyoruz. Velhasıl...

## Nasıl yüklerim?

[![PyPI version](https://badge.fury.io/py/sinkaf.svg)](https://badge.fury.io/py/sinkaf)
![PyPI - Downloads](https://img.shields.io/pypi/dm/sinkaf?color=orange)

```python
pip install sinkaf
```

## Nasıl kullanırım?

```python
from sinkaf import Sinkaf
  
snf = Sinkaf()

snf.tahmin(["çok tatlı çocuk", "çok şerefsiz çocuk"])
# array([False,  True])

snf.tahminlik(["çok tatlı çocuk", "çok şerefsiz çocuk"])
# array([0.09811712, 0.86237484])
```

### Alternatif model
```python
snf = Sinkaf(model = "BERT")

snf.tahmin(["çok tatlı çocuk", "çok şerefsiz çocuk"])
# array([False,  True])

snf.tahminlik(["çok tatlı çocuk", "çok şerefsiz çocuk"])
# array([0.26865139 0.85412345])

```

## İyi çalışıyor mu?
Fena değil gibi ama tabi daha iyi kesinlikle olabilir. 

Detaylar için:   
- [`sinkaf()`](sinkaf.ipynb)
- [`sinkaf(model = "BERT")`](sinkaf_alternatif.ipynb)