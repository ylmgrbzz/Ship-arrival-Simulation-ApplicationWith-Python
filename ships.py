import pandas as pd
import tkinter as tk
from tkinter import scrolledtext
import emoji

# Excel dosyasını oku
df = pd.read_excel('ships.xlsx')

# GUI Oluşturma
root = tk.Tk()
root.title("Simülasyon Uygulaması")

# Verileri ekrana yazdırmak için bir etiket (Label) oluştur
label_text = df.to_string(index=False)
label_text_with_emoji = emoji.emojize("\U0001F6A9 " + label_text.replace('\n', '\n\U0001F6A9 '))
label = scrolledtext.ScrolledText(root, width=80, height=20)
label.insert(tk.END, label_text_with_emoji)
label.pack()

# Gemi Varış Noktasında butonunu oluştur
def gemi_varis_noktasinda():
    # İlk sıradaki gemiyi listeden kaldır
    df.drop(df.index[0], inplace=True)
    
    # Yeni sıralamayı hesapla
    df['New Ranking'] = range(1, len(df) + 1)
    
    # Verileri güncelle
    label.delete(1.0, tk.END)
    updated_label_text = df.to_string(index=False)
    updated_label_text_with_emoji = emoji.emojize("\U0001F6A9 " + updated_label_text.replace('\n', '\n\U0001F6A9 '))
    label.insert(tk.END, updated_label_text_with_emoji)

# Gemi Varış Noktasında butonunu ekleyin
gemi_varis_noktasinda_button = tk.Button(root, text="Ship at Destination", command=gemi_varis_noktasinda)
gemi_varis_noktasinda_button.pack()

# GUI'yi başlat
root.mainloop()

