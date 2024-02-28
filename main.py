import streamlit as st
import pandas as pd
import altair as alt
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
#load dataset
test_df=pd.read_csv('data_capstone_new0.csv')
test_df['tahun']=pd.to_datetime(test_df['tahun'])
test_df['tahun'] = test_df['tahun'].apply(lambda x: x.strftime('%Y'))
test_df['tahun_dum']=test_df['tahun']
#data manipulation variable tahun dummy untuk membuat variabel filter tahun
test_df['tahun_dum']=pd.to_numeric(test_df['tahun_dum'])
#copy dataset
df_copy=test_df.copy()
# df_copy.info()
#melakukan tahapan cleansing dengan mengganti value NULL dengan 0, pertimbangan data tidak di delete karena masih diperlukan dalam analisa
df_copy=df_copy.fillna(0)
# df_copy.info()
# melakukan manipulasi data 
df_copy['jml_wisatawan']=df_copy['wisatawan_lokal']+df_copy['wisatawan_asing']
df_copy['jml_odtw']=df_copy['jumlah_odtw_Alam']+df_copy['jumlah_odtw_Budaya']+df_copy['jumlah_odtw_Minat_Khusus']+df_copy['jumlah_odtw_Buatan']
df_copy['jml_pendapatan_wisata']=df_copy['Pendapatan_Hotel']+df_copy['Pendapatan_Restoran_Rumah_Makan']+df_copy['Pendapatan_Hiburan']+df_copy['Pendapatan_Retribusi']
df_copy['jml_hotel']=df_copy['Hotel_Bintang1']+df_copy['Hotel_Bintang2']+df_copy['Hotel_Bintang3']+df_copy['Hotel_Bintang4']+df_copy['Hotel_Bintang5']+df_copy['Hotel_Non_Bintang']
st.title("Apakah banyaknya objek destinasi tempat wisata akan mempengaruhi jumlah kunjungan wisata di kota atau kabupaten provinsi Jawa Barat?")
st.markdown("")
st.markdown("")
st.markdown("sumber:")
st.markdown("""[https://opendata.jabarprov.go.id/](https://opendata.jabarprov.go.id/)
            """)
st.markdown("")
#text wording info
st.markdown("Provinsi Jawa Barat dikenal masyarakat sebagai tempat tujuan destinasi objek wisata, Hal ini karena faktor keindahan Alam, Budaya dan keanekaragaman Kuliner\
            yang secara tidak langsung dapat mempengaruhi pendapatan daerah dari sektor wisata. Dari Hal tersebut banyak beberapa kota/kabupaten yang membuka objek destinasi wisata baru baik \
            wisata alam/budaya/minat khusus/buatan sehingga harapannya dapat meningkatan jumlah kunjungan wisatawan ke daerah tersebut. Untuk mengetahui apakah ada **pengaruh/keterkaitan jumlah wisatawan dengan \
            banyaknya jumlah destinasi objek wisata** di kota/kabupaten Jawa Barat. Berikut sebaran jumlah wisatawan dari beberapa tahun kebelakang di kota/kabupaten/Provinsi Jawa Barat ")
st.markdown("")
#membuat filter object kota/kabupaten/provinsi dashboard
kota=st.selectbox("Pilih Object",("JAWA BARAT","KABUPATEN BOGOR","KABUPATEN SUKABUMI","KABUPATEN CIANJUR","KABUPATEN BANDUNG","KABUPATEN GARUT","KABUPATEN TASIKMALAYA","KABUPATEN CIAMIS","KABUPATEN KUNINGAN","KABUPATEN CIREBON","KABUPATEN MAJALENGKA","KABUPATEN SUMEDANG","KABUPATEN INDRAMAYU","KABUPATEN SUBANG","KABUPATEN PURWAKARTA","KABUPATEN KARAWANG","KABUPATEN BEKASI","KABUPATEN BANDUNG BARAT","KOTA BOGOR","KOTA SUKABUMI","KOTA BANDUNG","KOTA CIREBON","KOTA BEKASI","KOTA DEPOK","KOTA CIMAHI","KOTA TASIKMALAYA","KOTA BANJAR","KABUPATEN PANGANDARAN"))
st.markdown("")
#membuat slider tahun dashboard
z=st.slider("Range Tahun",2013,2022,(2016,2020))
tahun_0=z[0]
tahun_1=z[1]
#melakukan manipulasi data
df_copy1=df_copy[(df_copy['tahun_dum']>=tahun_0)&(df_copy['tahun_dum']<=tahun_1)]
df_copy_sel=df_copy1[(df_copy1['kabupaten_kota_prov']==kota)&(df_copy1['tahun']!='2013')]
df_copy_sel1=df_copy1[(df_copy1['tahun']!='2013')&(df_copy['kabupaten_kota_prov']==kota)]

#membuat grafik line Jumlah Wisatawan Dashboard
line_wisatawan=alt.Chart(df_copy_sel[df_copy_sel['kabupaten_kota_prov']==kota],title="Jumlah Wisatawan - "+kota).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).encode(
    alt.X('tahun',title='Tahun',axis=alt.Axis(labelAngle=0)),
    alt.Y('jml_wisatawan',title='Wisatawan (Orang)')
)
st.altair_chart(line_wisatawan,theme=None,use_container_width=True)
#text wording info
st.markdown("Secara umum dalam **kurun waktu 2014-2022**, untuk jumlah wisatawan **dari tahun 2019 sampai 2021** di beberapa kota/kabupaten di Jawa Barat mengalami **anomali penurunan** kunjungan wisatawan hal ini\
            dikarenakan di **periode tersebut terjadi wabah penyakit covid-19** di seluruh kota di Indonesia, Namun setelah wabah covid-19 berakhir dan peraturan jaga jarak/social distancing\
            ditiadakan pemerintah memberikan kelonggaran kepada wisatawan untuk berkunjung ke berbagai tempat objek wisata sehingga perlahan jumlah wisatawan di tahun 2022 kembali pulih.")
st.markdown("")
st.markdown("")
#membuat grafik batang Jumlah Objek Destinasi Wisata Dashboard
bar_chart_odtw=alt.Chart(df_copy_sel[df_copy_sel['kabupaten_kota_prov']==kota],title="Jumlah Objek Destinasi Tempat Wisata - "+kota).mark_bar().encode(
    alt.X('tahun',title='Tahun',axis=alt.Axis(labelAngle=0)),
    alt.Y('jml_odtw',title='Jumlah Objek Wisata (#)')
)
st.altair_chart(bar_chart_odtw,theme=None,use_container_width=True)
#text wording info
st.markdown("Adapun **Jumlah Objek Destinasi Tempat Wisata (odtw)** dari **kurun waktu tahun 2014-2022 mengalami peningkatan** di beberapa kota/kabupaten wilayah provinsi Jawa Barat, sehingga **perlu di cek kembali apakah peningkatan jumlah destinasi objek wisata\
            akan mempengaruhi jumlah kedatangan wisatawan atau ada pengaruh faktor penunjang lain (hotel/kuliner)** di tempat tersebut sehingga pendapatan dari sektor pariwisata juga mengalami peningkatan.")
st.markdown("")
st.markdown("")
# membuat Grafik Pendapatan Sektor Wisata Dashboard
chart_area_pendapatan = alt.Chart(df_copy_sel[df_copy_sel['kabupaten_kota_prov']==kota],title="Pendapatan Sektor Wisata - "+kota).mark_area(point=alt.OverlayMarkDef(filled=False, fill="white"),opacity=0.4).encode(
    alt.X('tahun',title='Tahun',axis=alt.Axis(labelAngle=0)),
    alt.Y('jml_pendapatan_wisata',title='Rupiah')
    )
st.altair_chart(chart_area_pendapatan,use_container_width=True)
#text wording info
st.markdown("Untuk mengetahui hubungan antara jumlah wisatawan dengan jumlah objek destinasi tempat wisata (odtw), dilakukan **uji korelasi dalam rentang tahun 2019-2022**, dengan **pertimbangan:\
            peningkatan yang signifikan** terhadap jumlah wisatawan, terutama setelah wabah pandemi berakhir di tahun 2022, berikut untuk heatmap-korelasi:")
st.markdown("")
#Membuat filter tahun untuk dashboard heatmap korelasi dan teman-temannya
z1=st.slider("Range Tahun",2014,2022,(2016,2020))
tahun_filt_0=z1[0]
tahun_filt_1=z1[1]
#melakukan manipulasi data untuk mempersiapkan data korelasi
df_copy2=df_copy[(df_copy['tahun_dum']>=tahun_filt_0)&(df_copy['tahun_dum']<=tahun_filt_1)]
df_copy_sel1=df_copy2[(df_copy['tahun']!='2013')&(df_copy2['kabupaten_kota_prov']!="JAWA BARAT")]
df_copy_sel2=df_copy_sel1.copy()
df_transform=df_copy_sel2.rename(columns={"jml_wisatawan":"wisatawan","jml_odtw":"odtw","jml_hotel":"hotel","Jum_Unit_Usaha_Restoran":"Usaha_Restoran","jml_pendapatan_wisata":"pendapatan_wisata"})
df_transform['kabupaten_kota_prov']=df_transform['kabupaten_kota_prov'].str.replace('KABUPATEN','KAB')
needed_column=['wisatawan','pendapatan_wisata']
df_transf_sum_0=df_transform.groupby('kabupaten_kota_prov')[needed_column].mean()
df_transf_sum_0.reset_index(inplace=True)
df_copy3=df_transform[df_transform["tahun_dum"]==tahun_filt_1]
df_copy3=pd.DataFrame(df_copy3[["kabupaten_kota_prov","odtw","hotel","Usaha_Restoran"]])
merge_df_transf=pd.merge(left=df_transf_sum_0,right=df_copy3,left_on='kabupaten_kota_prov',right_on="kabupaten_kota_prov")

#membuat grafik buble chart untuk melihat keterkaitan jumlah wisatawan, objek wisata dan pendapatan wisata
chart_buble=alt.Chart(merge_df_transf,title="Grafik Buble terkait Wisatawan, Objek Destinasi Wisata, Pendapatan Wisata di Kota/Kabupaten").mark_point(filled=True,opacity=0.7).encode(
    alt.X('wisatawan',title="wisatawan (orang)"),
    alt.Y('odtw',title="objek wisata (#)"),
    color='kabupaten_kota_prov',
    size='pendapatan_wisata',
).properties(height=400)

#manipulasi dan membuat grafik heatmap korelasi 
df_corr=df_transform[["wisatawan","odtw","hotel","Usaha_Restoran","pendapatan_wisata"]].corr()
plt.figure(figsize=(12,1.5))
plot=sns.heatmap(df_corr,cmap="Blues",annot=True)
st.pyplot(plot.get_figure())

#text wording info
st.markdown("")
st.markdown("")
st.markdown("Berdasarkan hasil Uji **Korelasi antara jumlah wisatawan dengan jumlah objek destinasi wisata** dengan **nilai korelasi adalah +0.15 yang artinya keterkaitan korelasinya lemah,\
            jumlah objek destinasi tempat wisata sedikit berpengaruh terhadap kenaikan jumlah wisatawan**, namun meningkatnya jumlah wisatawan dapat **disebabkan adanya faktor lain** semisal\
            fasilitas tempat menginap/hotel atau kuliner khas di daerah tersebut.")
st.markdown("Dalam hal ini terlihat diantara **nilai hasil uji korelasi jumlah wisatawan terhadap variabel hotel dan kuliner**, ternyata **nilai korelasi jumlah wisatawan lebih kuat terhadap variabel hotel yaitu +0.58** artinya **wisatawan yang berkunjung ke suatu daerah\
            kemungkinan juga mempertimbangkan faktor lain** seperti dari sisi fasilitas/layanan tempat menginap/hotel, bisa saja wisatawan tersebut hanya ingin staycation untuk istirahat atau memanfaatkan promo-promo dari beberapa hotel.")
st.markdown("Sedangkan untuk **variabel kuliner terhadap jumlah wisatawan nilai korelasinya lemah +0.087** namun **korelasi variabel kuliner terhadap pendapatan wisata memiliki nilai korelasi yang kuat +0.76** artinya **tujuan utama orang berkunjung ke suatu daerah bukan untuk kuliner(mencari makanan khas)**,\
            namun ketika wisatawan berkunjung ke suatu daerah secara tidak langsung mereka akan melakukan kegiatan kuliner di sekitar daerah tersebut, sehingga usaha kuliner secara tidak langsung mempengaruhi peningkatan pendapatan sektor pariwisata.")
st.markdown("")
st.markdown("")

# Membuat grafik Pendapatan Sektor Wisata Kota/Kabupaten Level
bar_chart_pendapatan_kab=alt.Chart(df_transform,title="Pendapatan Sektor Wisata Kota/Kabupaten Level").mark_bar().encode(
    x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
    y=alt.Y("mean(pendapatan_wisata):Q",title="Rupiah")
)
st.altair_chart(bar_chart_pendapatan_kab,theme=None,use_container_width=True)

# text info wording
st.markdown("Dari **Profile Pendapatan Sektor Wisata di level Kota/Kabupaten** Jawa Barat rentang **waktu 2019-2022, Kota Bekasi memiliki jumlah pendapatan tertinggi** sekitar 1 Triliun rupiah dengan sekitar 3 juta wisatawan dan 60 destinasi objek wisata yang lebih sedikit jika dibandingkan dengan sekitar 29 juta wisatawan dan 68 objek destinasi wisata di Kota Bandung.\
            Sedangkan untuk pendapatan sektor wisatanya sendiri Kota Bandung berada di posisi nomer 3 sekitar 340 Milyar rupiah, Hal ini menunjukan bahwa **banyaknya objek destinasi wisata di suatu daerah kurang berpengaruh secara signifikan terhadap peningkatan jumlah wisatawan**.")
st.markdown("")
st.markdown("")

st.altair_chart(chart_buble,theme=None,use_container_width=True)
#membuat detail sebaran per kabupaten untuk wisatawan, objek wisata, hotel, usaha_restoran level kabupaten
bar_chart_wisata=alt.Chart(df_transform).mark_bar().encode(
    alt.X("sum(wisatawan):Q",title="wisatawan (orang)"),
    y=alt.Y("kabupaten_kota_prov",title="kota/kabupaten",sort='-x')
)
bar_chart_odtw_kab=alt.Chart(merge_df_transf).mark_bar().encode(
    alt.X("odtw",title="Objek Wisata (#)"),
    y=alt.Y("kabupaten_kota_prov",title="kota/kabupaten",sort='-x')
)
bar_chart_Usaha_Restoran=alt.Chart(merge_df_transf).mark_bar().encode(
    alt.X("Usaha_Restoran",title="Restoran (#)"),
    y=alt.Y("kabupaten_kota_prov",title="kota/kabupaten",sort='-x')
)
bar_chart_hotel=alt.Chart(merge_df_transf).mark_bar().encode(
    alt.X("hotel",title="Hotel (#)"),
    y=alt.Y("kabupaten_kota_prov",title="kota/kabupaten",sort='-x')
)
#text info wording
st.markdown("Sedangkan untuk sebaran jumlah wisata/odtw/usaha restoran/hotel di masing-masing kota/kabupaten, menunjukan tidak ada kecenderungan suatu kota memenuhi kriteria tersebut, berikut detailnya:")
st.markdown("")

#container untuk detail sebaran grafik 
col1,col2,col3,col4=st.columns(4,gap="small")
col1.altair_chart(bar_chart_wisata,use_container_width=True,theme=None)
col2.altair_chart(bar_chart_odtw_kab,use_container_width=True,theme=None)
col3.altair_chart(bar_chart_Usaha_Restoran,use_container_width=True,theme=None)
col4.altair_chart(bar_chart_hotel,use_container_width=True,theme=None)

st.markdown("Dari hasil uraian analisa dan pengamatan diatas, dapat dipahami bahwa **tingkat pengaruh jumlah objek destinasi wisata masih kurang berdampak terhadap\
            peningkatan jumlah wisatawan** serta pendapatan sektor pariwisata Kota/Kabupaten di Provinsi Jawa Barat, Oleh karena itu sebagai bahan masukan untuk pemerintah daerah\
            bisa melakukan pendalaman/kajian lebih lanjut terhadap:")
st.markdown("""
            - Melakukan peninjauan kondisi objek wisata di area, apakah diperlukan perbaikan dari kondisi lingkungan/fisik tempat wisata/ melakukan eksplorasi edukasi objek wisata melalui iklan media sosial
            - Melakukan kerjasama dengan pihak ketiga semisal pengusaha tempat penginapan/hotel, dengan memberikan promo atau event di tempat-tempat objek wisata sehingga menarik minat wisatawan untuk berkunjung
            - Memberdayakan usaha kuliner/UMKM di lingkungan objek wisata dengan melibatkan aspek warga sekitar, Harapannya dengan semakin banyak usaha kuliner di daerah wisata dapat meningkatkan pendapatan sektor wisata
"""
)

