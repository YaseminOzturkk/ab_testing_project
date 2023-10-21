#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchase metriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’inin ayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBidding uygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur

# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Gerekli Kütüphaneler

import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# !pip install statsmodels
import statsmodels.stats.api as sms
from scipy.stats import ttest_1samp, shapiro, levene, ttest_ind, mannwhitneyu, \
    pearsonr, spearmanr, kendalltau, f_oneway, kruskal
from statsmodels.stats.proportion import proportions_ztest

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 10)
pd.set_option('display.float_format', lambda x: '%.5f' % x)

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz.
# Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

control_df = pd.read_excel("ABTesti/ab_testing.xlsx", sheet_name="Control Group")
test_df = pd.read_excel("ABTesti/ab_testing.xlsx", sheet_name="Test Group")

df_control = control_df.copy()
df_test = test_df.copy()

# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

def check_df(dataframe, head=5):
    print("###################### SHAPE #########")
    print(dataframe.shape)
    print("###################### TYPES #########")
    print(dataframe.dtypes)
    print("###################### HEAD #########")
    print(dataframe.head())
    print("###################### TAIL #########")
    print(dataframe.tail())
    print("###################### NA #########")
    print(dataframe.isnull().sum())
    print("###################### SUMMARY STATISTICS #########")
    print(dataframe.describe().T)
check_df(df_control)
check_df(df_test)



# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.

df_control["Group"] = 'Control'
df_test["Group"] = 'Test'
df_control.head()

df = pd.concat([df_control, df_test], axis=0, ignore_index=True)
df.head(50)


#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

# H0: M1 = M2 (Kontrol grubu ile test grubunun satın alma ortalamaları arasında ist. olarak anlamlı bir fark yoktur.)
# H1: M1 != M2 (Kontrol grubu ile test grubunun satın alma ortalamaları arasında ist. olarak anlamlı bir fark vardır)


# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

df.groupby('Group').agg({'Purchase': "mean"})


#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.
# Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

############################
# Normallik Varsayımı
############################

# H0: Normal dağılım varsayımı sağlanmaktadır.
# H1:..sağlanmamaktadır.


test_stat, pvalue = shapiro(df.loc[df["Group"] == "Control", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))

# p-value = 0.5891
# p-value < ise 0.05'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

#### Normal dağılım varsayımına göre HO reddedilemez, Yani normal dağılıyor.


############################
# Varyans Homojenligi Varsayımı
############################

# H0: Varyanslar Homojendir
# H1: Varyanslar Homojen Değildir

test_stat, pvalue = levene(df.loc[df["Group"] == "Control", "Purchase"],
                           df.loc[df["Group"] == "Test", "Purchase"])
print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


# p-value = 0.1083
# p-value < ise 0.05 'ten HO RED.
# p-value < değilse 0.05 H0 REDDEDILEMEZ.

#### Normal dağılım varsayımına göre HO reddedilemez, Yani normal dağılıyor.


# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

################  CEVAP #######################
# Her iki varsayım da sağlandığı için bağımsız iki örneklem t testini(parametrik test) uygulayabiliriz.


# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

test_stat, pvalue = ttest_ind(df.loc[df["Group"] == "Control", "Purchase"],
                              df.loc[df["Group"] == "Test", "Purchase"],
                              equal_var=True)

print('Test Stat = %.4f, p-value = %.4f' % (test_stat, pvalue))


################  CEVAP #######################
# p-value = 0.3493
# p-value değeri 0.005'ten büyüktür. Bu durumda HO hipotezini reddedemeyiz. Bu da kontrol ve test gruplarının satın alma
# ortalamaları arasında istatistiksel olarak anlamlı bir fark olmadığını gösterir.


##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.
###################### CEVAP ##############################
# Normallik Varsayımı aşamasında scipy kütüphanesindeki shapiro metodunu kullandık,
# Varyans Homojenliği aşamasında scipy kütüphanesinden levene metodunu kullandık ve elde ettiğimiz
# p_value değeri'lerinin varsayımları sağladığını gördük ve bağımsız iki örnekli t testinin (parametrik test) uygun
# olduğuna karar verdik.



# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.

# Sonuç olarak bombabomba.com'un yeni bir özelliği test etmek için yaptığı A/B testinde istatistiksel açıdan anlamlı bir
# fark bulunmamakta. Anlamlı bir fark olmadığından müşteriye her iki yöntemi de kullanmasını önerebiliriz.