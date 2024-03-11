import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
from vega_datasets import data

st.set_page_config(layout="wide")
#load dataset
sheet_url = 'https://docs.google.com/spreadsheets/d/15QN_oRbiRt2s3q-Om9_cNLiqjZp2GdwhYuBilA38Jcs/edit#gid=1715675833'
sheet_url_trf = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')
test_df=pd.read_csv(sheet_url_trf)
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
df_copy['Pendapatan_Hotel']=df_copy['Pendapatan_Hotel']/1000000000
df_copy['Pendapatan_Restoran_Rumah_Makan']=df_copy['Pendapatan_Restoran_Rumah_Makan']/1000000000
df_copy['Pendapatan_Hiburan']=df_copy['Pendapatan_Hiburan']/1000000000
df_copy['Pendapatan_Retribusi']=df_copy['Pendapatan_Retribusi']/1000000000

# df_copy.info()
# melakukan manipulasi data 
df_copy['jml_wisatawan']=df_copy['wisatawan_lokal']+df_copy['wisatawan_asing']
df_copy['jumlah_odtw_Minat_Khusus_Buatan']=df_copy['jumlah_odtw_Minat_Khusus']+df_copy['jumlah_odtw_Buatan']
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
st.markdown("Provinsi Jawa Barat dikenal masyarakat sebagai tempat tujuan destinasi objek wisata, Hal ini karena faktor keindahan Alam, Budaya dan Keanekaragaman Kuliner\
            yang secara tidak langsung dapat mempengaruhi pendapatan daerah dari sektor pariwisata. Berangkat dari hal tersebut banyak beberapa pemerintah daerah kota/kabupaten\
            yang membuka objek destinasi wisata baru baik wisata alam/budaya/minat khusus/buatan sehingga harapannya dapat meningkatan jumlah kunjungan wisatawan ke daerah tersebut.\
            Untuk mengetahui tentang **seberapa pengaruh peningkatan jumlah objek wisata terhadap kunjungan jumlah wisatawan** di kota/kabupaten Jawa Barat berikut sebaran jumlah wisatawan\
            dari beberapa tahun kebelakang di kota/kabupaten/Provinsi Jawa Barat :")
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
line_detail_wisatawan=alt.Chart(df_copy_sel[df_copy_sel['kabupaten_kota_prov']==kota],title="Wisatawan by Kategori - "+kota).mark_line(point=alt.OverlayMarkDef(filled=False, fill="white")).transform_fold(
    fold=['wisatawan_asing', 'wisatawan_lokal'], 
    as_=['kategori', 'total']
).encode(
    alt.X('tahun',title='Tahun',axis=alt.Axis(labelAngle=0)),
    y='total:Q',
    color=alt.Color('kategori:N',legend=alt.Legend(orient='bottom',titleAnchor='middle',direction='horizontal')),
)
tab_wisata1,tab_wisata2,tab_wisata3=st.tabs(["Total Wisatawan","Kategori Wisatawan","Kategori Wisatawan per Kota/Kabupaten"])
with tab_wisata1:
    st.altair_chart(line_wisatawan,use_container_width=True)
with tab_wisata2:
    st.altair_chart(line_detail_wisatawan,theme=None,use_container_width=True)
with tab_wisata3:
    option1=st.selectbox("Pilih Tahun",("2014","2015","2016","2017","2018","2019","2020","2021","2022"),index=None,key="1")
    df_copy3=df_copy[(df_copy['tahun']==option1)&(df_copy['kabupaten_kota_prov']!="JAWA BARAT")]
    bar_chart_total=alt.Chart(df_copy3,title="Jumlah Wisatawan").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("jml_wisatawan:Q",title="orang"),
        tooltip=["kabupaten_kota_prov","jml_wisatawan","tahun"]
        )    
    bar_chart_asing=alt.Chart(df_copy3,title="Wisatawan Asing").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("wisatawan_asing:Q",title="orang"),
        tooltip=["kabupaten_kota_prov","wisatawan_asing","tahun"]
        )
    bar_chart_lokal=alt.Chart(df_copy3,title="Wisatawan Lokal").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("wisatawan_lokal:Q",title="orang"),
        tooltip=["kabupaten_kota_prov","wisatawan_lokal","tahun"]
        )
    st.altair_chart(bar_chart_total,theme=None,use_container_width=True)
    colw1,colw2=st.columns(2,gap="small")
    colw1.altair_chart(bar_chart_asing,theme=None,use_container_width=True)
    colw2.altair_chart(bar_chart_lokal,theme=None,use_container_width=True)
#text wording info
st.markdown("Kategori **kunjungan wisatawan dari tahun ke tahun dominasi dari wisatawan lokal** dengan terlihat pada **tahun 2022** paling banyak kunjungan \
            **wisatawan lokal dari kabupaten Subang** dan **wisatawan asing** paling banyak dari **Kabupaten Bekasi**.")
st.markdown("Secara umum dalam **kurun waktu 2014-2022**, untuk jumlah kunjungan wisatawan **dari tahun 2019 sampai 2021** di beberapa kota/kabupaten di Jawa Barat mengalami **anomali penurunan** \
            kunjungan wisata hal ini dikarenakan pada **periode tersebut terjadi wabah penyakit covid-19** di seluruh wilayah kota di Indonesia, Namun setelah wabah covid-19 berakhir dan peraturan \
            jaga jarak/social distancing oleh pemerintah diberi kelonggaran kepada wisatawan untuk berkunjung ke berbagai tempat objek wisata sehingga perlahan jumlah kunjungan wisatawan di tahun 2022 kembali pulih.")
st.markdown("")
st.markdown("")

#membuat grafik batang Jumlah Objek Destinasi Wisata Dashboard
bar_chart_odtw=alt.Chart(df_copy_sel[df_copy_sel['kabupaten_kota_prov']==kota],title="Jumlah Objek Destinasi Tempat Wisata - "+kota).mark_bar().encode(
    alt.X('tahun',title='Tahun',axis=alt.Axis(labelAngle=0)),
    alt.Y('jml_odtw',title='Jumlah Objek Wisata (#)')
)
bar_chart_odtw_detail=alt.Chart(df_copy_sel[df_copy_sel['kabupaten_kota_prov']==kota],title="Objek Destinasi Tempat Wisata - "+kota).mark_bar().transform_fold(
    fold=['jumlah_odtw_Alam', 'jumlah_odtw_Budaya','jumlah_odtw_Minat_Khusus_Buatan'], 
    as_=['kategori', 'total']
).encode(
    alt.X('tahun',title='Tahun',axis=alt.Axis(labelAngle=0)),
    y=alt.Y('total:Q'),
    color=alt.Color('kategori:N',legend=alt.Legend(orient='bottom',titleAnchor='middle',direction='horizontal')),
)

tab_odtw_detail1,tab_odtw_detail2,tab_odtw_detail3=st.tabs(["Objek Destinasi Tempat Wisata","Kategori Objek Destinasi Tempat Wisata","Kategori Objek Destinasi Tempat Wisata per Kota/Kabupaten"])
with tab_odtw_detail1:
    st.altair_chart(bar_chart_odtw,theme=None,use_container_width=True)
with tab_odtw_detail2:
    st.altair_chart(bar_chart_odtw_detail,theme=None,use_container_width=True)
with tab_odtw_detail3:
        option2=st.selectbox("Pilih Tahun",("2014","2015","2016","2017","2018","2019","2020","2021","2022"),index=None,key="2")
        df_copy4=df_copy[(df_copy['tahun']==option2)&(df_copy['kabupaten_kota_prov']!="JAWA BARAT")]
        bar_chart_odtw_kab=alt.Chart(df_copy4,title="Objek Destinasi Wisata").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("jml_odtw:Q",title="#"),
        tooltip=["kabupaten_kota_prov","jml_odtw","tahun"],
        )
        bar_chart_odtw_alam=alt.Chart(df_copy4,title="Objek Destinasi Wisata - Alam").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("jumlah_odtw_Alam:Q",title="#"),
        tooltip=["kabupaten_kota_prov","jumlah_odtw_Alam","tahun"],
        )
        bar_chart_odtw_budaya=alt.Chart(df_copy4,title="Objek Destinasi Wisata - Budaya").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("jumlah_odtw_Budaya:Q",title="#"),
        tooltip=["kabupaten_kota_prov","jumlah_odtw_Budaya","tahun"],
        )
        bar_chart_odtw_minatkhusus=alt.Chart(df_copy4,title="Objek Destinasi Wisata - Minat Khusus/Buatan").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("jumlah_odtw_Minat_Khusus_Buatan:Q",title="#"),
        tooltip=["kabupaten_kota_prov","jumlah_odtw_Minat_Khusus_Buatan","tahun"],
        )
        st.altair_chart(bar_chart_odtw_kab,theme=None,use_container_width=True)
        colodw1,colodw2,colodw3=st.columns(3,gap="small")
        colodw1.altair_chart(bar_chart_odtw_alam,theme=None,use_container_width=True)
        colodw2.altair_chart(bar_chart_odtw_budaya,theme=None,use_container_width=True)
        colodw3.altair_chart(bar_chart_odtw_minatkhusus,theme=None,use_container_width=True)
#text wording info
st.markdown("Adapun **Jumlah Objek Destinasi Tempat Wisata (odtw)** dari **kurun waktu tahun 2014-2022 mengalami peningkatan** di beberapa kota/kabupaten wilayah provinsi Jawa Barat. Dengan dominasi objek wisata yg paling diminati adalah wisata Alam.")
st.markdown("**Pada tahun 2022**, secara jumlah Objek Destinasi Wisata paling banyak di **kabupaten Bandung**. Namun **secara Kategori** untuk destinasi **wisata Alam masih paling diminati** di kabupaten Pangandaran\
            dan untuk kabupaten Bandung wisatawan lebih tertarik dengan objek tempat wisata Budaya.")
st.markdown("Sehingga perlu di cek kembali pengaruh jumlah destinasi objek wisata terhadap jumlah kunjungan wisatawan atau ada pengaruh faktor lain (semisal hotel/kuliner) di tempat tersebut sehingga pendapatan dari sektor pariwisata juga mengalami peningkatan.")
st.markdown("")
st.markdown("")

# membuat Grafik Pendapatan Sektor Wisata Dashboard
chart_area_pendapatan = alt.Chart(df_copy_sel[df_copy_sel['kabupaten_kota_prov']==kota],title="Pendapatan Sektor Wisata - "+kota).mark_area(point=alt.OverlayMarkDef(filled=False, fill="white"),opacity=0.4).encode(
    alt.X('tahun',title='Tahun',axis=alt.Axis(labelAngle=0)),
    alt.Y('jml_pendapatan_wisata',title='Rupiah (Milyar)')
    )
chart_detail_pendapatan=alt.Chart(df_copy_sel[df_copy_sel['kabupaten_kota_prov']==kota],title="Pendapatan Wisata by Kategori - "+kota).mark_area(opacity=0.6).transform_fold(
    fold=['Pendapatan_Hotel', 'Pendapatan_Restoran_Rumah_Makan','Pendapatan_Hiburan','Pendapatan_Retribusi'], 
    as_=['kategori', 'total']
).encode(
    alt.X('tahun',title='Tahun',axis=alt.Axis(labelAngle=0)),
    y=alt.Y('total:Q',title='Rupiah (Milyar)'),
    color=alt.Color('kategori:N',legend=alt.Legend(orient='bottom',titleAnchor='middle',direction='horizontal')))
tab_pend_wisata1,tab_pend_wisata2,tab_pend_wisata3=st.tabs(["Pendapatan Wisata","Kategori Pendapatan Wisata","Kategori Pendapatan Wisata per Kota/Kabupaten"])
with tab_pend_wisata1:
    st.altair_chart(chart_area_pendapatan,use_container_width=True)
with tab_pend_wisata2:
    st.altair_chart(chart_detail_pendapatan,theme=None,use_container_width=True)
with tab_pend_wisata3:
        option3=st.selectbox("Pilih Tahun",("2014","2015","2016","2017","2018","2019","2020","2021","2022"),index=None,key="3")
        df_copy5=df_copy[(df_copy['tahun']==option3)&(df_copy['kabupaten_kota_prov']!="JAWA BARAT")]
        bar_chart_pend_total=alt.Chart(df_copy5,title="Pendapatan Wisata").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("jml_pendapatan_wisata:Q",title='Rupiah (Milyar)'),
        tooltip=["kabupaten_kota_prov","jml_pendapatan_wisata","tahun"],
        )
        bar_chart_pend_hotel=alt.Chart(df_copy5,title="Pendapatan Hotel").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("Pendapatan_Hotel:Q",title='Rupiah (Milyar)'),
        tooltip=["kabupaten_kota_prov","Pendapatan_Hotel","tahun"],
        )
        bar_chart_pend_rumah_makan=alt.Chart(df_copy5,title="Pendapatan Restoran Rumah Makan").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("Pendapatan_Restoran_Rumah_Makan:Q",title='Rupiah (Milyar)'),
        tooltip=["kabupaten_kota_prov","Pendapatan_Restoran_Rumah_Makan","tahun"],
        )
        bar_chart_pend_hiburan=alt.Chart(df_copy5,title="Pendapatan Hiburan").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("Pendapatan_Hiburan:Q",title='Rupiah (Milyar)'),
        tooltip=["kabupaten_kota_prov","Pendapatan_Hiburan","tahun"],
        )
        bar_chart_pend_retribusi=alt.Chart(df_copy5,title="Pendapatan Retribusi").mark_bar().encode(
        x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
        y=alt.Y("Pendapatan_Retribusi:Q",title='Rupiah (Milyar)'),
        tooltip=["kabupaten_kota_prov","Pendapatan_Retribusi","tahun"],
        )
        st.altair_chart(bar_chart_pend_total,theme=None,use_container_width=True)
        colpw1,colpw2=st.columns(2,gap="small")
        colpw1.altair_chart(bar_chart_pend_hotel,theme=None,use_container_width=True)
        colpw2.altair_chart(bar_chart_pend_rumah_makan,theme=None,use_container_width=True)
        colpw3,colpw4=st.columns(2,gap="small")
        colpw3.altair_chart(bar_chart_pend_hiburan,theme=None,use_container_width=True)
        colpw4.altair_chart(bar_chart_pend_retribusi,theme=None,use_container_width=True)

#text wording info
st.markdown("Pendapatan daerah dari sektor wisata di provinsi Jawa Barat mengalami pertumbuhan, pada tahun 2022 kontribusi pendapatan wisata tertinggi dari Restoran Rumah Makan, terjadi di kota Bekasi.")
st.markdown("Namun jika melihat dari jumlah kunjungan wisatawan/objek destinasi wisata, Kunjungan wisata Kota Bekasi tidak sepadat Kota Subang atau sebanyak objek wisata di kabupaten Bandung.")
st.markdown("Sehingga dari beberapa hal uraian diatas, perlu dilakukan pengamatan lebih dalam terhadap profil sebaran data antara jumlah wisatawan dengan jumlah objek destinasi tempat wisata (odtw)\
            atau dengan faktor lain misal hotel, usaha restoran-makanan, agar dapat melihat seberapa pengaruh jumlah objek wisata terhadap jumlah kunjungan wisata. Pengamatan dilakukan dalam rentang tahun 2019-2022,\
            dengan pertimbangan: peningkatan yang signifikan terhadap jumlah wisatawan, terutama setelah wabah pandemi berakhir di tahun 2022, berikut sebaran data:")
st.markdown("")
#Membuat filter tahun untuk dashboard heatmap korelasi dan teman-temannya
z1=st.slider("Range Tahun",2014,2022,(2019,2022))
tahun_filt_0=z1[0]
tahun_filt_1=z1[1]

#melakukan manipulasi data untuk mempersiapkan data korelasi
df_copy2=df_copy[(df_copy['tahun_dum']>=tahun_filt_0)&(df_copy['tahun_dum']<=tahun_filt_1)]
df_copy_sel1=df_copy2[(df_copy['tahun']!='2013')&(df_copy2['kabupaten_kota_prov']!="JAWA BARAT")]
df_copy_sel2=df_copy_sel1.copy()
df_transform=df_copy_sel2.rename(columns={"jml_wisatawan":"wisatawan","jml_odtw":"odtw","jml_hotel":"hotel","Jum_Unit_Usaha_Restoran":"Usaha_Restoran","jml_pendapatan_wisata":"pendapatan_wisata"})
df_transform['kabupaten_kota_prov']=df_transform['kabupaten_kota_prov'].str.replace('KABUPATEN','KAB')
needed_column=['wisatawan','pendapatan_wisata']
df_transf_sum_0=df_transform.groupby('kabupaten_kota_prov')[needed_column].agg({'wisatawan':'sum','pendapatan_wisata':'mean'})
df_transf_sum_0.reset_index(inplace=True)
df_copy3=df_transform[df_transform["tahun_dum"]==tahun_filt_1]
df_copy3=pd.DataFrame(df_copy3[["kabupaten_kota_prov","odtw","hotel","Usaha_Restoran"]])
merge_df_transf=pd.merge(left=df_transf_sum_0,right=df_copy3,left_on='kabupaten_kota_prov',right_on="kabupaten_kota_prov")

#scater wisatawan terhadap variable lain
chart_scatter1 = alt.Chart(df_transform).mark_circle(size=60).encode(
        alt.X('odtw',title="odtw(#)"),
        alt.Y('wisatawan',title="wisatawan(orang)"),
        # color='Origin',
        # tooltip=['odtw', 'wisatawan', 'tahun','kabupaten_kota_prov'],
    )
chart_scatter2 = alt.Chart(df_transform).mark_circle(size=60).encode(
        alt.X('hotel',title="hotel(#)"),
        alt.Y('wisatawan',title="wisatawan(orang)"),
        tooltip=['hotel', 'wisatawan', 'tahun','kabupaten_kota_prov'],
    )
chart_scatter3 = alt.Chart(df_transform).mark_circle(size=60).encode(
        alt.X('Usaha_Restoran',title="Usaha_Restoran(#)"),
        alt.Y('wisatawan',title="wisatawan(orang)"),
        tooltip=['Usaha_Restoran', 'wisatawan', 'tahun','kabupaten_kota_prov'],
    )

#scater pendapatan terhadap variable lain
chart_scatter4 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='wisatawan',
        y='pendapatan_wisata',
        tooltip=['wisatawan', 'pendapatan_wisata', 'tahun','kabupaten_kota_prov'],
        # color='Origin',
        # tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
    )
chart_scatter5 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='odtw',
        y='pendapatan_wisata',
        tooltip=['odtw', 'pendapatan_wisata', 'tahun','kabupaten_kota_prov'],
    )
chart_scatter6 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='hotel',
        y='pendapatan_wisata',
        tooltip=['hotel', 'pendapatan_wisata', 'tahun','kabupaten_kota_prov'],
    )
chart_scatter7 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='Usaha_Restoran',
        y='pendapatan_wisata',
        tooltip=['Usaha_Restoran', 'pendapatan_wisata', 'tahun','kabupaten_kota_prov'],
    )

#scater Usaha_Restoran terhadap variable lain
chart_scatter8 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='wisatawan',
        y='Usaha_Restoran',
        tooltip=['odtw', 'Usaha_Restoran', 'tahun','kabupaten_kota_prov'],
        # color='Origin',
        # tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
    )
chart_scatter9 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='odtw',
        y='Usaha_Restoran',
        tooltip=['hotel', 'Usaha_Restoran', 'tahun','kabupaten_kota_prov'],
    )
chart_scatter10 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='hotel',
        y='Usaha_Restoran',
        tooltip=['wisatawan', 'Usaha_Restoran', 'tahun','kabupaten_kota_prov'],
    )

#scater Objek Destinasi terhadap variable lain
chart_scatter11 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='wisatawan',
        y='odtw',
        tooltip=['wisatawan', 'odtw', 'tahun','kabupaten_kota_prov'],
        # color='Origin',
        # tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
    )
chart_scatter12 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='hotel',
        y='odtw',
        tooltip=['hotel', 'odtw', 'tahun','kabupaten_kota_prov'],
    )
chart_scatter13 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='Usaha_Restoran',
        y='odtw',
        tooltip=['Usaha_Restoran', 'odtw', 'tahun','kabupaten_kota_prov'],
    )
#scater Hotel terhadap variable lain
chart_scatter14 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='wisatawan',
        y='hotel',
        tooltip=['wisatawan', 'hotel', 'tahun','kabupaten_kota_prov'],
        # color='Origin',
        # tooltip=['Name', 'Origin', 'Horsepower', 'Miles_per_Gallon']
    )
chart_scatter15 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='odtw',
        y='hotel',
        tooltip=['odtw', 'hotel', 'tahun','kabupaten_kota_prov'],
    )
chart_scatter16 = alt.Chart(df_transform).mark_circle(size=60).encode(
        x='Usaha_Restoran',
        y='hotel',
        tooltip=['Usaha_Restoran', 'hotel', 'tahun','kabupaten_kota_prov'],
    )

st.markdown("")
st.markdown("Scatterplot :")
tab1,tab4,tab5,tab3,tab2=st.tabs(["Jumlah Wisatawan","Objek Wisata","Hotel","Usaha Restoran","Pendapatan Wisata"])
with tab1:
    col_1,col_2,col_3=st.columns(3,gap="small")
    col_1.altair_chart(chart_scatter1+chart_scatter1.transform_regression('odtw','wisatawan').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_2.altair_chart(chart_scatter2+chart_scatter2.transform_regression('hotel','wisatawan').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_3.altair_chart(chart_scatter3+chart_scatter3.transform_regression('Usaha_Restoran','wisatawan').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
with tab2:
    col_4,col_5,col_6,col_7=st.columns(4,gap="small")
    col_4.altair_chart(chart_scatter4+chart_scatter4.transform_regression('wisatawan','pendapatan_wisata').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_5.altair_chart(chart_scatter5+chart_scatter5.transform_regression('odtw','pendapatan_wisata').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_6.altair_chart(chart_scatter6+chart_scatter6.transform_regression('hotel','pendapatan_wisata').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_7.altair_chart(chart_scatter7+chart_scatter7.transform_regression('Usaha_Restoran','pendapatan_wisata').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
with tab3:
    col_8,col_9,col_10=st.columns(3,gap="small")
    col_8.altair_chart(chart_scatter8+chart_scatter8.transform_regression('wisatawan','Usaha_Restoran').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_9.altair_chart(chart_scatter9+chart_scatter9.transform_regression('odtw','Usaha_Restoran').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_10.altair_chart(chart_scatter10+chart_scatter10.transform_regression('hotel','Usaha_Restoran').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
with tab4:
    col_11,col_12,col_13=st.columns(3,gap="small")
    col_11.altair_chart(chart_scatter11+chart_scatter11.transform_regression('wisatawan','odtw').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_12.altair_chart(chart_scatter12+chart_scatter12.transform_regression('hotel','odtw').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_13.altair_chart(chart_scatter13+chart_scatter13.transform_regression('Usaha_Restoran','odtw').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
with tab5:
    col_14,col_15,col_16=st.columns(3,gap="small")
    col_14.altair_chart(chart_scatter14+chart_scatter14.transform_regression('wisatawan','hotel').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_15.altair_chart(chart_scatter15+chart_scatter15.transform_regression('odtw','hotel').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)
    col_16.altair_chart(chart_scatter16+chart_scatter16.transform_regression('Usaha_Restoran','hotel').mark_line(color='black',strokeDash=[4,2]),use_container_width=True,theme=None)

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

with st.expander("Korelasi Tabel"):
    st.pyplot(plot.get_figure())

#text wording info
st.markdown("")
st.markdown("")
st.markdown("Dari hasil pengamatan diagram scatter, terlihat pada tahun 2019-2022 pengaruh jumlah objek destinasi wisata terhadap jumlah kunjungan wisatawan menghasilkan pola sebaran data yang menyebar, dibandingkan dengan sebaran data pada pengaruh hotel/usaha kuliner terhadap jumlah kunjungan wisatawan.")
st.markdown("Hasil pola data sebaran yang menyebar ini menunjukan bahwa beberapa daerah yang mempunyai objek destinasi wisata banyak tetapi jumlah kunjungan wisatawannya masih sedikit. Berdasarkan uraian tersebut terlihat jumlah objek destinasi wisata kurang berpengaruh terhadap jumlah kunjungan wisata dan ada pengaruh faktor lain\
            selain jumlah destinasi objek wisata semisal hotel dan usaha makanan.")
st.markdown("")
st.markdown("")

# Membuat grafik Pendapatan Sektor Wisata Kota/Kabupaten Level
bar_chart_pendapatan_kab=alt.Chart(df_transform,title="Pendapatan Sektor Wisata Kota/Kabupaten Level").mark_bar().encode(
    x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
    y=alt.Y("mean(pendapatan_wisata):Q",title="Rupiah")
)

bar_chart_pend1=alt.Chart(df_transform,title="Pendapatan_Hotel").mark_bar().encode(
    x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
    y=alt.Y("mean(Pendapatan_Hotel):Q",title="Rupiah (Milyar)"),
)
bar_chart_pend2=alt.Chart(df_transform,title="Pendapatan_Restoran_Rumah_Makan").mark_bar().encode(
    x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
    y=alt.Y("mean(Pendapatan_Restoran_Rumah_Makan):Q",title="Rupiah (Milyar)")
)
bar_chart_pend3=alt.Chart(df_transform,title="Pendapatan_Hiburan").mark_bar().encode(
    x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
    y=alt.Y("mean(Pendapatan_Hiburan):Q",title="Rupiah (Milyar)")
)
bar_chart_pend4=alt.Chart(df_transform,title="Pendapatan_Retribusi").mark_bar().encode(
    x=alt.X("kabupaten_kota_prov",sort='-y',title="Kota/Kabupaten"),
    y=alt.Y("mean(Pendapatan_Retribusi):Q",title="Rupiah (Milyar)")
)

tab_kab_pend1,tab_kab_pend2=st.tabs(["Pendapatan Wisata Kota-Kabupaten","Kategori Pendapatan Wisata Kota-Kabupaten"])
with tab_kab_pend1:
    st.altair_chart(bar_chart_pendapatan_kab,theme=None,use_container_width=True)
with tab_kab_pend2:
    colp1,colp2=st.columns(2,gap="small")
    colp1.altair_chart(bar_chart_pend1,use_container_width=True,theme=None)
    colp2.altair_chart(bar_chart_pend2,use_container_width=True,theme=None)
    colp3,colp4=st.columns(2,gap="small")
    colp3.altair_chart(bar_chart_pend3,use_container_width=True,theme=None)
    colp4.altair_chart(bar_chart_pend4,use_container_width=True,theme=None)

# text info wording
st.markdown("Dari **Profile Pendapatan Sektor Wisata di level Kota/Kabupaten** Jawa Barat rentang **waktu 2019-2022, Kota Bekasi memiliki pendapatan daerah wisata tertinggi** sekitar 1 Triliun rupiah dengan sekitar 3 juta wisatawan dan 60 destinasi objek wisata yang lebih sedikit jika dibandingkan dengan sekitar 29 juta wisatawan dan 68 objek destinasi wisata di Kota Bandung.\
            Sedangkan untuk pendapatan sektor wisatanya sendiri Kota Bandung berada di posisi nomer 3 sekitar 340 Milyar rupiah, sumbangsih terbesar pendapatan terbesar dari Usaha Restoran-Rumah Makan/Hiburan/Retribusi.")
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
