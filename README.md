# A* and RL gym grid ortamı

2 boyutta tasarlanan grid üzerinde, bloklara çarpmadan hedef noktaya gidebilmek için rota planlama algoritmalarından A* ve RL metotlarından PPO karşılaştırılmıştır.


##### Gereklilikler
> CUDA 10.2 \
> Python 3.8 \

#### Gerekli kütüphane kurulumları
```
pip install -r requirements.txt
```

#### Wandb ayarları
Wandb’de hesap açın. Hesabınıza giriş yapıp New Project’e tıklayın. Bir isim verip
projenizi oluşturun. Verilen API KEY’i, kullanıcı adınızı ve projeye verdiğiniz ismi kaydedin. 

./PPO/train.py içinde aşağıdaki satırları güncelleyin.
```
os.environ["WANDB_API_KEY"] = "api key"
user = "who r u?"
project = "projeismi" 
```

Bu satırda başlattığınız eğitime bir isim verin. Yüzlerce eğitim olabileceğinden isimlendirme
yapınıza algoritma tipini ve hatırlatıcı parametreler ekleyin. 

```
display_name = "Astar&RL_PPO_Training_1"
```

#### Eğitimi başlat

```
cd ./PPO
python train.py