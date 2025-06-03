# Discord Multi-Account Message Bot

**Discord Multiple accounts and many messages bot**, tools buat auto kirim pesan ke channel discord make banyak akun dan banyak pesan (flexibel) secara pararel, kalo ada yang gagal gk ganggu akun lain. *cocok buat push level discord* 👍

# Features
Silahkan baca setiap perintah secara teliti saat running bot!!

1. **Mode Basic** <br>
    Auto kirim pesan dari awal hingga akhir make banyak akun (opsional)
2. **Mode Timer** <br>
    Auto kirim pesan dari awal hingga akhir dan balik lagi ke awal selama waktu timer belum tercapai. jika waktu timer sudah tercapai maka akan stop pada urutan pesan apapun!
3.   (coming soon!!)

# Installation
 * Python version 3.12 or later 

     ```bash
    git clone https://github.com/Meowstronot/discord_msg_bot.git
    cd discord_msg_bot
    pip install -r requirements.txt 
    ```
# Configuration
* `msg.txt`: Pastikan bahwa `msg.txt` berisi data yang sesuai dengan format yang dibutuhkan oleh skrip. Contoh format isi file:
     ```
    your_msg_1
    your_msg_2
    ```
* `token.txt`: Pastikan bahwa `token.txt` berisi data yang sesuai dengan format yang dibutuhkan oleh skrip. Contoh format isi file:
     ```
    your_dc_token_1
    your_dc_token_2
    ```
* After that  silahkan eksekusi bot make command
     ```bash
    python main.py
    ```
# HOW TO GET DISCORD TOKEN?
1. Login Discord di browser
2. Goto Developer Tools Page di browser (CTRL + SHIFT + i)
3. Pergi ke Network
4. Kirim pesan di chanel manapun
5. Cari Authorization di Request Header, lalu copy tokennya


    ![screenshot][def]
# Notes
* Token Discord akan kereset jika kalian logout akun
* Harus open browser buat run code? No, selama token discordnya gk kereset close browser aman
* Selalu cek token discordnya apabila kereset
* !! Simpan Token Discord Baik2 !! jangan sampe ke leak
* Pertanyaan lain silahkan DM [twitter](https://x.com/meowstronot)


[def]: get_token_dc.gif