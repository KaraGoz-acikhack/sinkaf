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

## Nasıl kullanırım?

Baya kolay yapmaya uğraştık ama daha yapmadık... şimdilik sadece modelimiz `sinkaf.ipynb` dosyasının içinde hazır duruyor.

Hazır olduğunda:
```python
from sinkaf import tahmin, tahminlik

tahmin("bok çocuksun.")
# True

tahmin("iyi çocuksun sen de ha!")
# False

tahminlik("bok çocuksun.")
# 0.95

tahminlik("iyi çocuksun sen de ha!")
# 0.05
```
tarzında bir kullanım bekleyebilirsiniz.