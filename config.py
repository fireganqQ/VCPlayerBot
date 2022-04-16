#!/usr/bin/env python3
# Copyright (C) @subinps
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
from utils import LOGGER
try:
   import os
   import heroku3
   from dotenv import load_dotenv
   from ast import literal_eval as is_enabled

except ModuleNotFoundError:
    import os
    import sys
    import subprocess
    file=os.path.abspath("requirements.txt")
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', file, '--upgrade'])
    os.execl(sys.executable, sys.executable, *sys.argv)


class Config:
    #Telegram API Stuffs
    load_dotenv()  # load enviroment variables from .env file
    ADMIN = os.environ.get("ADMINS", '')
    SUDO = [int(admin) for admin in (ADMIN).split()] # Exclusive for heroku vars configuration.
    ADMINS = [int(admin) for admin in (ADMIN).split()] #group admins will be appended to this list.
    API_ID = int(os.environ.get("API_ID", ''))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")     
    SESSION = os.environ.get("SESSION_STRING", "")

    #Stream Chat and Log Group
    CHAT = int(os.environ.get("CHAT", ""))
    LOG_GROUP=os.environ.get("LOG_GROUP", "")

    #Stream 
    STREAM_URL=os.environ.get("STARTUP_STREAM", "https://www.youtube.com/watch?v=zcrUCvBD16k")
   
    #Database
    DATABASE_URI=os.environ.get("DATABASE_URI", None)
    DATABASE_NAME=os.environ.get("DATABASE_NAME", "VCPlayerBot")


    #heroku
    API_KEY=os.environ.get("HEROKU_API_KEY", None)
    APP_NAME=os.environ.get("HEROKU_APP_NAME", None)


    #Optional Configuration
    SHUFFLE=is_enabled(os.environ.get("SHUFFLE", 'True'))
    ADMIN_ONLY=is_enabled(os.environ.get("ADMIN_ONLY", "False"))
    REPLY_MESSAGE=os.environ.get("REPLY_MESSAGE", False)
    EDIT_TITLE = os.environ.get("EDIT_TITLE", True)
    #others
    
    RECORDING_DUMP=os.environ.get("RECORDING_DUMP", False)
    RECORDING_TITLE=os.environ.get("RECORDING_TITLE", False)
    TIME_ZONE = os.environ.get("TIME_ZONE", "Asia/Kolkata")    
    IS_VIDEO=is_enabled(os.environ.get("IS_VIDEO", 'True'))
    IS_LOOP=is_enabled(os.environ.get("IS_LOOP", 'True'))
    DELAY=int(os.environ.get("DELAY", '10'))
    PORTRAIT=is_enabled(os.environ.get("PORTRAIT", 'False'))
    IS_VIDEO_RECORD=is_enabled(os.environ.get("IS_VIDEO_RECORD", 'True'))
    DEBUG=is_enabled(os.environ.get("DEBUG", 'False'))
    PTN=is_enabled(os.environ.get("PTN", "False"))

    #Quality vars
    E_BITRATE=os.environ.get("BITRATE", False)
    E_FPS=os.environ.get("FPS", False)
    CUSTOM_QUALITY=os.environ.get("QUALITY", "100")

    #Search filters for cplay
    FILTERS =  [filter.lower() for filter in (os.environ.get("FILTERS", "video document")).split(" ")]


    #Dont touch these, these are not for configuring player
    GET_FILE={}
    DATA={}
    STREAM_END={}
    SCHEDULED_STREAM={}
    DUR={}
    msg = {}

    SCHEDULE_LIST=[]
    playlist=[]
    CONFIG_LIST = ["ADMINS", "IS_VIDEO", "IS_LOOP", "REPLY_PM", "ADMIN_ONLY", "SHUFFLE", "EDIT_TITLE", "CHAT", 
    "SUDO", "REPLY_MESSAGE", "STREAM_URL", "DELAY", "LOG_GROUP", "SCHEDULED_STREAM", "SCHEDULE_LIST", 
    "IS_VIDEO_RECORD", "IS_RECORDING", "WAS_RECORDING", "RECORDING_TITLE", "PORTRAIT", "RECORDING_DUMP", "HAS_SCHEDULE", 
    "CUSTOM_QUALITY"]

    STARTUP_ERROR=None

    ADMIN_CACHE=False
    CALL_STATUS=False
    YPLAY=False
    YSTREAM=False
    CPLAY=False
    STREAM_SETUP=False
    LISTEN=False
    STREAM_LINK=False
    IS_RECORDING=False
    WAS_RECORDING=False
    PAUSE=False
    MUTED=False
    HAS_SCHEDULE=None
    IS_ACTIVE=None
    VOLUME=100
    CURRENT_CALL=None
    BOT_USERNAME=None
    USER_ID=None

    if LOG_GROUP:
        LOG_GROUP=int(LOG_GROUP)
    else:
        LOG_GROUP=None
    if not API_KEY or \
       not APP_NAME:
       HEROKU_APP=None
    else:
       HEROKU_APP=heroku3.from_key(API_KEY).apps()[APP_NAME]


    if EDIT_TITLE in ["NO", 'False']:
        EDIT_TITLE=False
        LOGGER.info("Title Editing turned off")
    if REPLY_MESSAGE:
        REPLY_MESSAGE=REPLY_MESSAGE
        REPLY_PM=True
        LOGGER.info("Reply Message Found, Enabled PM MSG")
    else:
        REPLY_MESSAGE=False
        REPLY_PM=False

    if E_BITRATE:
       try:
          BITRATE=int(E_BITRATE)
       except:
          LOGGER.error("Invalid bitrate specified.")
          E_BITRATE=False
          BITRATE=48000
       if not BITRATE >= 48000:
          BITRATE=48000
    else:
       BITRATE=48000
    
    if E_FPS:
       try:
          FPS=int(E_FPS)
       except:
          LOGGER.error("Invalid FPS specified")
          E_FPS=False
       if not FPS >= 30:
          FPS=30
    else:
       FPS=30
    try:
       CUSTOM_QUALITY=int(CUSTOM_QUALITY)
       if CUSTOM_QUALITY > 100:
          CUSTOM_QUALITY = 100
          LOGGER.warning("maximum quality allowed is 100, invalid quality specified. Quality set to 100")
       elif CUSTOM_QUALITY < 10:
          LOGGER.warning("Minimum Quality allowed is 10., Qulaity set to 10")
          CUSTOM_QUALITY = 10
       if  66.9  < CUSTOM_QUALITY < 100:
          if not E_BITRATE:
             BITRATE=48000
       elif 50 < CUSTOM_QUALITY < 66.9:
          if not E_BITRATE:
             BITRATE=36000
       else:
          if not E_BITRATE:
             BITRATE=24000
    except:
       if CUSTOM_QUALITY.lower() == 'high':
          CUSTOM_QUALITY=100
       elif CUSTOM_QUALITY.lower() == 'medium':
          CUSTOM_QUALITY=66.9
       elif CUSTOM_QUALITY.lower() == 'low':
          CUSTOM_QUALITY=50
       else:
          LOGGER.warning("Invalid QUALITY specified.Defaulting to High.")
          CUSTOM_QUALITY=100



    #help strings 
    PLAY_HELP="""
__Bu seçeneklerden herhangi birini kullanarak oynayabilirsiniz.__

1. Bir YouTube bağlantısından bir video oynatın.
Command: **/play**
__Bunu bir YouTube bağlantısına yanıt olarak veya bağlantıyı birlikte ilet komutu olarak kullanabilirsiniz. veya bunu YouTube'da aramak için iletiye yanıt olarak.__

2. Bir telgraf dosyasından oynatın.
Command: **/play**
__Desteklenen bir medyaya yanıt verin (video ve belgeler veya ses dosyası).__
Not: __Her iki durumda da /fplay ayrıca yöneticiler tarafından sıranın bitmesini beklemeden şarkıyı hemen çalmak için kullanılabilir.__

3. Bir YouTube oynatma listesinden oynatın
Command: **/yplay**
__Önce @GetPlaylistBot veya @DumpPlaylist'ten bir çalma listesi dosyası alın ve çalma listesi dosyasına yanıt verin.__

4. Canlı Akış
Command: **/stream**
__Akış olarak oynatmak için bir canlı yayın URL'si veya herhangi bir doğrudan URL iletin.__

5. Eski bir çalma listesini içe aktarın.
Command: **/import**
__Önceden dışa aktarılan bir oynatma listesi dosyasına yanıt verin. __

6. Kanal Oynatma
Command: **/cplay**
__Verilen kanaldaki tüm dosyaları oynatmak için `/cplay kanal kullanıcı adı veya kanal kimliği`ni kullanın.
Varsayılan olarak hem video dosyaları hem de belgeler oynatılacaktır. `FILTERS` değişkenini kullanarak dosya türünü ekleyebilir veya kaldırabilirsiniz.
Örneğin, kanaldan ses, video ve belge akışı yapmak için `/env FILTERS video belge sesi`ni kullanın. Yalnızca sese ihtiyacınız varsa, `/env FILTERS video audio` vb. öğelerini kullanabilirsiniz.
Bir kanaldaki dosyaları STARTUP_STREAM olarak ayarlamak, böylece dosyalar bot başlangıcında otomatik olarak oynatma listesine eklenecektir. `/env STARTUP_STREAM kanal kullanıcı adı veya kanal kimliği' kullanın

Herkese açık kanallar için '@' ile birlikte kanalların kullanıcı adını ve özel kanallar için kanal kimliğini kullanmanız gerektiğini unutmayın.
Özel kanallar için hem bot hem de KULLANICI hesabının kanalın üyesi olduğundan emin olun.__
"""
    SETTINGS_HELP="""
**Oyuncunuzu ihtiyaçlarınıza göre kolayca özelleştirebilirsiniz. Aşağıdaki konfigürasyonlar mevcuttur:**

🔹Command: **/settings**

🔹Mevcut YAPILANDIRMALAR:

**Oyuncu Modu** - __Bu, oynatıcınızı 7/24 müzik çalar olarak veya yalnızca sırada şarkı olduğunda çalıştırmanıza olanak tanır.
Devre dışı bırakılırsa, oynatma listesi boş olduğunda oyuncu aramadan çıkar.
Aksi takdirde, oynatma listesi kimliği boş olduğunda STARTUP_STREAM yayınlanır.__

**Video Etkin** - __Bu, ses ve video arasında geçiş yapmanızı sağlar.
devre dışı bırakılırsa, video dosyaları ses olarak oynatılacaktır.__

**Yalnızca Yönetici** - __Bunu etkinleştirmek, yönetici olmayan kullanıcıların oynatma komutunu kullanmasını kısıtlar.__

**Başlığı Düzenle** - __Bunu etkinleştirmek, VideoChat başlığınızı o anda çalmakta olan şarkı adına göre düzenler.__

**Karıştırma Modu** - __Bunu etkinleştirmek, bir oynatma listesini içe aktardığınızda veya /yplay'i kullandığınızda oynatma listesini karıştırır __

**Otomatik Yanıt** - __Oynayan kullanıcı hesabının PM mesajlarını yanıtlayıp yanıtlamamayı seçin.
`REPLY_MESSAGE` konfigürasyonunu kullanarak özel bir cevap mesajı oluşturabilirsiniz.__
"""
    SCHEDULER_HELP="""
__VCPlayer, bir akış planlamanıza olanak tanır.
Bu, gelecekteki bir tarih için bir akış planlayabileceğiniz ve planlanan tarihte akışın otomatik olarak oynatılacağı anlamına gelir.
Şu anda bir yıllık bir yayın akışı planlayabilirsiniz!!. Bir veritabanı kurduğunuzdan emin olun, aksi takdirde oynatıcı yeniden başladığında programlarınızı kaybedersiniz. __

Command: **/schedule**

__Bir dosyaya veya youtube videosuna veya hatta bir metin mesajına program komutuyla yanıt verin.
Cevaplanan medya veya youtube videosu planlanacak ve planlanan tarihte oynatılacaktır.
IST'de programlama zamanı varsayılandır ve 'TIME_ZONE' yapılandırmasını kullanarak saat dilimini değiştirebilirsiniz.__

Command: **/slist**
__Mevcut planlanmış akışlarınızı görüntüleyin.__

Command: **/cancel**
__Bir programı zamanlama kimliğine göre iptal edin, /slist komutunu kullanarak zamanlama kimliğini alabilirsiniz__

Command: **/cancelall**
__Planlanmış tüm akışları iptal edin__"""
    RECORDER_HELP="""
__VCPlayer ile tüm görüntülü sohbetlerinizi kolayca kaydedebilirsiniz.
Varsayılan olarak telgraf, maksimum 4 saat kayıt yapmanızı sağlar.
4 saat sonra kayıt otomatik olarak yeniden başlatılarak bu limit aşılmaya çalışılmıştır__

Command: **/record**

MEVCUT YAPILANDIRMALAR:
1. Video Kaydet: __Etkinleştirilirse, akışın hem videosu hem de sesi kaydedilir, aksi takdirde yalnızca ses kaydedilir.__

2. Video boyutu: __Kaydınız için dikey ve yatay boyutlar arasında seçim yapın__

3. Özel Kayıt Başlığı: __Kayıtlarınız için özel bir kayıt başlığı ayarlayın. Bunu yapılandırmak için /rtitle komutunu kullanın.
Özel başlığı kapatmak için `/rtitle False `__ kullanın

4. Kayıt Aptal: __Tüm kayıtlarınızı bir kanala iletmeyi ayarlayabilirsiniz, aksi takdirde kayıtlar akış hesabının kayıtlı mesajlarına gönderileceğinden bu yararlı olacaktır.
`RECORDING_DUMP` yapılandırmasını kullanarak kurulum.__

⚠️ vcplayer ile bir kayda başlarsanız, vcplayer ile aynı şeyi durdurduğunuzdan emin olun.
"""

    CONTROL_HELP="""
__VCPlayer, akışlarınızı kolayca kontrol etmenizi sağlar__
1. Bir şarkıyı atlayın.
Command: **/skip**
__Şarkıyı o konumda atlamak için 2'den büyük bir sayı iletebilirsiniz.__

2. Oynatıcıyı duraklatın.
Command: **/pause**

3. Oynatıcıyı devam ettirin.
Command: **/resume**

4. Ses Seviyesini Değiştirin.
Command: **/volume**
__Sesi 1-200 arasında geçirin.__

5. VC'den ayrılın.
Command: **/leave**

6. Çalma listesini karıştırın.
Command: **/shuffle**

7. Mevcut çalma listesi sırasını temizleyin.
Command: **/clearplaylist**

8. Videoyu arayın.
Command: **/seek**
__Atlanacak saniye sayısını geçebilirsiniz. Örnek: 10 saniye atlamak için /seek 10. / 10 saniye geri sarmak için -10 ara.__

9. Oynatıcıyı sessize alın.
Command: **/vcmute**

10. Oynatıcının sesini açın.
Command : **/vcunmute**

11. Çalma listesini gösterir.
Command: **/playlist** 
__Kontrol düğmeleriyle göstermek için /player'ı kullanın__
"""

    ADMIN_HELP="""
__VCPlayer, yöneticileri kontrol etmenizi sağlar, yani yönetici ekleyebilir ve kolayca kaldırabilirsiniz.
Daha iyi bir deneyim için bir MongoDb veritabanı kullanılması önerilir, aksi takdirde tüm yöneticileriniz yeniden başlattıktan sonra sıfırlanır.__

Command: **/vcpromote**
__Bir yöneticiyi, kullanıcı adı veya kullanıcı kimliği ile ya da o kullanıcı mesajına yanıt vererek terfi ettirebilirsiniz.__

Command: **/vcdemote**
__Yönetici listesinden bir yöneticiyi kaldırın__

Command: **/refresh**
__Sohbetin yönetici listesini yenileyin__"""

    MISC_HELP="""
Command: **/export**
__VCPlayer, mevcut çalma listenizi ileride kullanmak üzere dışa aktarmanıza olanak tanır.__
__Size bir json dosyası gönderilecek ve aynısı /import komutu ile birlikte kullanılabilir.__

Command : **/logs**
__Oyuncunuz bir şeyler ters gittiyse, /logs kullanarak günlükleri kolayca kontrol edebilirsiniz.__

Command : **/env**
__Yapılandırma değişkenlerinizi /env komutuyla ayarlayın.__
__Örnek: Bir __ `REPLY_MESSAGE` kurmak için __use__ `/env REPLY_MESSAGE=Hey, PM'ime spam göndermek yerine @subin_works'e göz atın`__
__Bir yapılandırma değişkenini bunun için bir değer atlayarak silebilirsiniz, Örnek:__ `/env LOG_GROUP=` __bu, mevcut LOG_GROUP yapılandırmasını siler.__

Command: **/config**
__/env** kullanımıyla aynı

Command: **/update**
__En son değişikliklerle botunuzu günceller__

İpucu: __Kullanıcı hesabını ve bot hesabını başka bir gruba ve yeni gruptaki herhangi bir komutu ekleyerek CHAT yapılandırmasını kolayca değiştirebilirsiniz__
"""
    ENV_HELP="""
**Bunlar, mevcut yapılandırılabilir değişkenlerdir ve her birini /env komutunu kullanarak ayarlayabilirsiniz**

**Zorunlu Değişkenler**
1. "API_ID" : __[my.telegram.org'dan](https://my.telegram.org/) alınız__
2. `API_HASH` : __[my.telegram.org'dan](https://my.telegram.org/) alınız__

3. `BOT_TOKEN` : __[@Botfather](https://telegram.dog/BotFather)__

4. `SESSION_STRING` : __Generate From here [GenerateStringName](https://repl.it/@subinps/getStringName)__

5. `CHAT` : __Bot'un Müzik çaldığı Kanalın/Grubun Kimliği.__

6. `STARTUP_STREAM` : __Bu, botun başlatılması ve yeniden başlatılması sırasında yayınlanacak.
Herhangi bir STREAM_URL'yi veya herhangi bir videonun doğrudan bağlantısını veya bir Youtube Canlı bağlantısını kullanabilirsiniz.
Ayrıca YouTube Oynatma Listesini de kullanabilirsiniz. Oynatma listeniz için [PlayList Dumb](https://telegram.dog/DumpPlaylist) adresinden bir Telegram Bağlantısı bulabilir veya [PlayList Extract](https://telegram.dog/GetAPlaylistbot) adresinden bir Oynatma Listesi alabilirsiniz. .
Oynatma Listesi bağlantısı "https://t.me/DumpPlaylist/xxx" biçiminde olmalıdır.
Bir kanaldaki dosyaları başlangıç akışı olarak da kullanabilirsiniz. Bunun için STARTUP_STREAM değeri olarak kanalın kanal kimliğini veya kanal kullanıcı adını kullanın.
Kanal oynatma hakkında daha fazla bilgi için oynatıcı bölümündeki yardımı okuyun.__

**Önerilen Opsiyonel Değişkenler**

1. `DATABASE_URI`: __MongoDB veritabanı URL'si, [mongodb](https://cloud.mongodb.com) adresinden alın. Bu isteğe bağlı bir değişkendir, ancak tüm özellikleri deneyimlemek için bunu kullanmanız önerilir.__

2. `HEROKU_API_KEY`: __Heroku API anahtarınız. [Buradan](https://dashboard.heroku.com/account/applications/authorizations/new)__ bir tane edinin

3. `HEROKU_APP_NAME`: __Heroku uygulamanızın adı.__

4. `FILTERS`: __Kanal oynatma dosyası araması için filtreler. Oynatıcı bölümündeki cplay ile ilgili yardımı okuyun.__

**Diğer Opsiyonel Değişkenler**
1. `LOG_GROUP` : __CHAT bir Grup ise Oynatma Listesi gönderilecek grup__

2. `ADMINS` : __Yönetici komutlarını kullanabilen kullanıcıların kimliği.__

3. `REPLY_MESSAGE` : __Kullanıcı hesabına PM ile mesaj atanlara cevap. Bu özelliğe ihtiyacınız yoksa boş bırakın. (Mongodb eklendiyse düğmeler aracılığıyla yapılandırılabilir. /ayarları kullanın)__

4. `ADMIN_ONLY` : __Pass `True` Sadece `CHAT` yöneticileri için /play komutu vermek istiyorsanız. Varsayılan olarak /play herkes için mevcuttur.(Mongodb eklendiyse düğmeler aracılığıyla yapılandırılabilir. /ayarları kullanın)__

5. `DATABASE_NAME`: __mongodb veritabanınız için veritabanı adı.mongodb__

6. `SHUFFLE` : __Çalma listelerini karıştırmak istemiyorsanız 'Yanlış' yapın. (Düğmeler aracılığıyla yapılandırılabilir)__

7. `EDIT_TITLE` : __Bot'un çalan şarkıya göre görüntülü sohbet başlığını düzenlemesini istemiyorsanız 'Yanlış' yapın. (Mongodb eklendiyse düğmeler aracılığıyla yapılandırılabilir. /ayarları kullanın)__

8. `RECORDING_DUMP` : __Görüntülü sohbet kayıtlarını boşaltmak için yönetici olarak KULLANICI hesabı olan bir Kanal Kimliği.__

9. `RECORDING_TITLE`: __Görüntülü sohbet kayıtlarınız için özel bir başlık.__

10. `TIME_ZONE` : __Ülkenizin Saat Dilimi, varsayılan olarak IST__

11. `IS_VIDEO_RECORD` : __Video kaydetmek istemiyorsanız 'Yanlış' yapın ve yalnızca ses kaydedilecektir.(Mongodb eklendiyse düğmeler aracılığıyla yapılandırılabilir. /kaydet kullan)__

12. `IS_LOOP` ; __7/24 Görüntülü Sohbet istemiyorsanız 'Yanlış' yapın. (Mongodb eklendiyse düğmeler aracılığıyla yapılandırılabilir. /ayarları kullanın)__

13. `IS_VIDEO` : __Çaları videosuz bir müzik çalar olarak kullanmak istiyorsanız 'Yanlış' yapın. (Mongodb eklendiyse düğmeler aracılığıyla yapılandırılabilir. /ayarları kullanın)__

14. `PORTRAIT`: __Video kaydını portre modunda istiyorsanız 'Doğru' yapın. (Mongodb eklendiyse butonlarla yapılandırılabilir. /record kullanın)__

15. `DELAY` : __Komutların silinmesi için zaman sınırını seçin. varsayılan olarak 10 saniye.__

16. `QUALITY` : __Görüntülü sohbetin kalitesini özelleştirin, aşağıdakilerden birini kullanın: `high`, `medium`, `low`.__

17. `BITRATE` : __Ses bit hızı (değiştirilmesi önerilmez).__

18. `FPS` : __ Oynatılacak videonun Fps'si (Değiştirilmesi önerilmez.)__

"""
