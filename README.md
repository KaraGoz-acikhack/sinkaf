# sinkaf

> _"Kötü söz sahibine aittir."_
>
> -Anonim


## Nedir?

`sinkaf` uygunsuz yorumların bulunmasını sağlayan bir python kütüphanesidir.

## Farkı nedir?

Diğer algoritmalardan en büyük farkı, önceden belirlenmiş bir kelime listesinden yorumlardaki sözcükleri tek tek kontrol etmek yerine, makine öğrenmesi metodları kullanarak cümlenin genel anlamına bakabilmesidir. Aynı zamanda `sinkaf` baya bi hızlı! 

## Nasıl çalışıyor?

Arka planda modelimizi eğitmek için [A corpus of Turkish offensive language](https://coltekin.github.io/offensive-turkish/guidelines.html) verisetini kullanıyoruz. Bu veriseti 36,000+ twitter yorumunun hakaret içerip içermediğini gösteren, Türkçe ile makine öğrenmesi denemeleri yapmak isteyenler için fevkaledenin fevkinde bir kaynak! Kendilerine teşekkür ediyoruz. Velhasıl...

## Nasıl yüklerim?
```python
pip install sinkaf
```

## Nasıl kullanırım?

```python
from sinkaf import tahmin, tahminlik

tahmin(["cok tatli cocuk", "cok serefsiz cocuk"])
# array([False,  True])

tahminlik(["cok tatli cocuk", "cok serefsiz cocuk"])
# array([0.04837164, 0.74293361])
```

## İyi çalışıyor mu?
Fena değil gibi ama tabi daha iyi kesinlikle olabilir. Detaylar için bkz. [link](sinkaf.ipynb)