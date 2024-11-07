import customtkinter as ctk
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk
import sqlite3
import io
import pickle

import pandas as pd

# Configurações iniciais
ctk.set_appearance_mode("Light")

# Connection with SQLite data base 
def db_connection():
    connection = sqlite3.connect('db_Agenda.db')
    return connection

# Creating Table
def create_table():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('''
CREATE TABLE IF NOT EXISTS tb_Pessoa (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    FirstName TEXT NOT NULL,
    SurName TEXT NOT NULL,
    Email TEXT,
    Phone_1 TEXT NOT NULL,
    Phone_2 TEXT,
    Image BLOB,
    Observation TEXT
    )
''')
    connection.commit()
    connection.close()

# CRUD Funtions

def create_contact(firstname_value, surname_value, email_value, phone1_value, phone2_value, image_link, observation_value):
    with open(image_link, 'rb') as file:
        img_blob = file.read()
        print(f'\n\nCREATE_CONTACT image_link = {image_link}\nimage_blob = {img_blob}\n\n')
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('''
INSERT INTO tb_Pessoa (FirstName, SurName, Email, Phone_1, Phone_2, Image, Observation)
VALUES (?, ?, ?, ? , ?, ?, ?)
''', (firstname_value, surname_value, email_value, phone1_value, phone2_value, img_blob, observation_value))
    connection.commit()
    connection.close()
    messagebox.showinfo('Sucesso','Contacto Cadastrado!')
    
def fetch_agenda():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT ID, FirstName, SurName, Email, Phone_1, Phone_2, Observation FROM tb_Pessoa')
    agenda = cursor.fetchall()
    connection.close()
    return agenda

def update_contact(id, firstname_value, surname_value, email_value, phone1_value, phone2_value, image_link, observation_value):
    #with open(image_link, 'rb') as file:
    #    img_blob = file.read()
    phone1_value = str(phone1_value)
    phone2_value = str(phone2_value)
    image_link = pickle.dumps(image_link)  # Serializa a tupla em formato binário

    print(f'\n\n{type(image_link)}\n\n')
    print(f'\n\nCREATE_CONTACT image_link = {image_link}\n\n')
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('''
UPDATE tb_Pessoa SET FirstName=?, SurName=?, Email=?, Phone_1=?, Phone_2=?, Image = ?, Observation=?
WHERE id=?
''', (firstname_value, surname_value, email_value, phone1_value, phone2_value, image_link, observation_value, id))
    connection.commit()
    connection.close()
    messagebox.showinfo('Sucesso','Contacto Editado!')

def delete_contact(id):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute('DELETE FROM tb_Pessoa WHERE ID=?', (id,))
    connection.commit()
    connection.close()
    messagebox.showinfo('Sucesso','Contacto Deletado!')
    
def search_contact(search):
    #load_image_by_id(id_value)
    connection = db_connection()
    cursor = connection.cursor()
    print(f'\n\n{search}\n\n')
    cursor.execute('SELECT ID, FirstName, SurName, Email, Phone_1, Phone_2, Observation FROM tb_Pessoa WHERE FirstName LIKE ? OR SurName LIKE ? OR Phone_1 LIKE ? OR Phone_2 LIKE ?', ('%'+search+'%', '%'+search+'%', '%'+search+'%', '%'+search+'%'))
    agenda = cursor.fetchall()
    connection.close()
    return agenda

def load_image_by_id(self, id):
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute(f'SELECT Image FROM tb_Pessoa WHERE ID = ?',(id,))
    registro = cursor.fetchone()
    
    if registro:
        img_blob = registro[0]
        img = Image.open(io.BytesIO(img_blob))
        img = img.resize((200, 100))  # Redimensiona a imagem se necessário
        img_tk = ImageTk.PhotoImage(img)

        # Atualiza o rótulo com a nova imagem
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk
    connection.close()
    return registro



class Program(tk.Tk):

    def clear_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
    
    
    def clear(self):
        pass
    
    global img
    
    
    def clear_image(self):
        self.image_label.config(image=None)
        self.image_label.image = None  # Remove a referência da imagem

    
    def load_image(self):
        print('\n\nQuase\n\n')
        # Abre o diálogo para escolher uma imagem
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg;*.jpeg;*.png;*.gif")])
        
        try:
            image = Image.open(file_path)
        except FileNotFoundError:
            print("Arquivo não encontrado.")
            return
        except OSError:
            print("Formato de arquivo inválido.")
            return
        
        
        self.img = file_path
        print(f'\n\nEntrei\n{file_path}\n')
        if file_path:
            # Carrega a imagem
            image = Image.open(file_path)
        
            # Define o novo tamanho
            new_size = (200, 100)  # Largura e altura desejadas
            image = image.resize(new_size)  # Redimensiona a imagem

            # Converte a imagem para o formato do Tkinter
            photo = ImageTk.PhotoImage(image)

            # Exibe a imagem no Label
            self.image_label.config(image=photo, bg='#B99352')
            self.image_label.image = photo  # '#FFDAA0' Mantém uma referência à imagem
    
    def __init__(self):
        super().__init__()
        self.title('Agenda De Contactos')
        self.geometry('700x610')
        self.config(bg='#FFDAA0')  # Define a cor de fundo
        #self.config(font=('Cambria Code', 12))  # Definindo texto default
        self.iconbitmap('Images/python_icon_188903.ico')
        self.resizable(0,0)
        
        # Creating the Table if Not Exists
        create_table()
        
        # Variaveis
        id_value = StringVar()
        firstname_value = StringVar()
        surname_value = StringVar()
        email_value = StringVar()
        phone1_value = StringVar()
        phone2_value = StringVar()
        obs_value = StringVar()
        search_value = StringVar()
        
        def nutrying_entrys(item):
            id_value.set(item[0])
            firstname_value.set(item[1])
            surname_value.set(item[2])
            email_value.set(item[3])
            phone1_value.set(item[4])
            phone2_value.set(item[5])
            self.img = load_image_by_id(self, item[0])
            print(f'\n\nNUTRYING_ENTRYS img = {self.img}\n\n')
            obs_value.set(item[6])
            search_value.set('')
        
        
        def get_selected_row(event):
            # Obtém o item selecionado
            selected_item = self.tree.selection()
            if selected_item:
                item = self.tree.item(selected_item)
                values = item['values']
                print("Linha Selecionada:", values)  # Aqui você pode fazer o que precisar com os valores
            
                # Adding list of the list to entrys
                nutrying_entrys(values)
            else:
                print("Nenhuma linha selecionada")
                messagebox.showwarning('Atenção','Precisa clicar a linha do contacto à selecionar.')
   
        
        def clear():
            id_value.set('')
            firstname_value.set('')
            surname_value.set('')
            email_value.set('')
            phone1_value.set('')
            phone2_value.set('')
            obs_value.set('')
            search_value.set('')
            restart_text()
            self.clear_image()


        def create():
            self.create()
            clear()
        def update():
            self.update()
            clear()
        def delete():
            self.delete()
            clear()
            
        def restart_text():
            self.id_entry.configure(placeholder_text='ID')
            self.firstname_entry.configure(placeholder_text='Nome')
            self.surname_entry.configure(placeholder_text='Sobrenome')
            self.email_entry.configure(placeholder_text='Email')
            self.phone1_entry.configure(placeholder_text='Telefone 1')
            self.phone2_entry.configure(placeholder_text='Telefone 2')
            self.obs_entry.configure(placeholder_text='Observações')



        
        # Frame Cad
        self.input_frame = tk.Frame(self, width=680, height=250, bg ='#B99352')
        self.input_frame.place(x=10, y=10)#, fill='x')
        self.input_label = ctk.CTkLabel(self.input_frame, text='Cadastros De Contactos', font=('Cascadia Code',18))
        self.input_label.place(y=5, x=250)
        
        # Label's
        
        self.id_label = ctk.CTkLabel(self.input_frame, text='ID', font=('Cascadia',12))
        self.id_label.place(x=20, y=40)
        self.firstname_label = ctk.CTkLabel(self.input_frame, text='Nome', font=('Cascadia',12))
        self.firstname_label.place(x=220, y=40)
        self.surname_label = ctk.CTkLabel(self.input_frame, text='Sobrenome', font=('Cascadia',12))
        self.surname_label.place(x=445, y=40)
        self.email_label = ctk.CTkLabel(self.input_frame, text='Email', font=('Cascadia',12))
        self.email_label.place(x=20, y=80)
        self.phone1_label = ctk.CTkLabel(self.input_frame, text='Telefone 1', font=('Cascadia',12))
        self.phone1_label.place(x=220, y=80)
        self.phone2_label = ctk.CTkLabel(self.input_frame, text='Telefone 2', font=('Cascadia',12))
        self.phone2_label.place(x=445, y=80)
        
        # Entry's
        
        self.id_entry = ctk.CTkEntry(self, textvariable=id_value, placeholder_text='ID', font=('Cascadia',12))
        self.id_entry.place(x=80, y=50)
        self.firstname_entry = ctk.CTkEntry(self, textvariable=firstname_value, placeholder_text='Nome')
        self.firstname_entry.place(x=300, y=50)
        self.surname_entry = ctk.CTkEntry(self, textvariable=surname_value, placeholder_text='Sobre Nome')
        self.surname_entry.place(x=530, y=50)
        self.email_entry = ctk.CTkEntry(self, textvariable=email_value, placeholder_text='Email')
        self.email_entry.place(x=80, y=90)
        self.phone1_entry = ctk.CTkEntry(self, textvariable=phone1_value, placeholder_text='Telefone 1')
        self.phone1_entry.place(x=300, y=90)
        self.phone2_entry = ctk.CTkEntry(self, textvariable=phone2_value, placeholder_text='Telefone 2')
        self.phone2_entry.place(x=530, y=90)
        
        # Carregando Imagem
        self.load_image_button = tk.Button(self.input_frame, text="Carregar Imagem", command=self.load_image, bg='#fff')
        self.load_image_button.place(x=60, y=220)
        
        # Cria um Label para exibir a imagem
        self.image_label = tk.Label(self.input_frame)
        self.image_label.place(x=10, y=120)
        
        # Entrada De Observações
        self.obs_label = ctk.CTkLabel(self.input_frame, text='Observações', font=('Arial',12))
        self.obs_label.place(x=215, y=120)
        self.obs_entry = ctk.CTkEntry(self, textvariable=obs_value, placeholder_text='Descrição', width=370, height=100, font=('Arial',14), border_color='#aaa', border_width=2)
        self.obs_entry.place(x=300, y=130)
        
        # Buttons of CreateUpdateDelete

        self.add_button = ctk.CTkButton(self, text="Cadastrar", command=create, width=120, fg_color='green')
        self.add_button.place(x=80,y=265)

        self.update_button = ctk.CTkButton(self, text="Atualizar", command=update, width=120)
        self.update_button.place(x=215,y=265)

        self.delete_button = ctk.CTkButton(self, text="Deletar", command=delete, width=120, fg_color='red')
        self.delete_button.place(x=350,y=265)
        
        self.clear_button = ctk.CTkButton(self, text="Limpar", command=clear, width=120, fg_color='gray')
        self.clear_button.place(x=485,y=265)
        
        # Frame Cad
        self.output_frame = tk.Frame(self, width=680, height=270, bg ='#B99352')
        self.output_frame.place(x=10, y=300)#, fill='x')
        self.output_label = ctk.CTkLabel(self, text='Lista De Contactos', font=('Cascadia Code',18), fg_color='#B99352')
        self.output_label.place(x=260, y=305)
        
        # Listing Data's
        
                # Lista de produtos com Treeview
        self.tree = ttk.Treeview(self, columns=('ID', 'Nome', 'Sobrenome', 'Email', 'Telefone 1', 'Telefone 2', 'Observações'), show='headings')
        self.tree.place(x=20, y=370, width=660, height=160)

        # Definir cabeçalhos e larguras das colunas
        colunas = {
            'ID': 50,
            'Nome': 100,
            'Sobrenome': 100,
            'Email': 100,
            'Telefone 1': 100,
            'Telefone 2': 100,
            'Observações': 110,
        }

        for col, largura in colunas.items():
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center", width=largura)

        # (Opcional) Defina a largura da Treeview como um todo
        self.tree.place(x=20, y=370)
        
        # Pushing the camps of entrys behind a event 'def get_selected_row(event)'
        self.tree.bind('<<TreeviewSelect>>', get_selected_row)

        
        '''
        # Lista de produtos com Treeview
        self.tree = ttk.Treeview(self, columns=('ID', 'Nome', 'Sobrenome', 'Email', 'Telefone 1', 'Telefone 2', 'Observações'), show='headings')
        self.tree.place(x=20, y=370, width=660, height=160)

        # Definir cabeçalhos
        for col in ('ID', 'Nome', 'Sobrenome', 'Email', 'Telefone 1', 'Telefone 2', 'Observações'):
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")
        
        #self.fetch_agenda()
        '''

        
        
        
        self.search_entry = ctk.CTkEntry(self, textvariable=search_value, placeholder_text="Nome, Telefone 1, Telefone 2", width=220)
        self.search_entry.place(x=250, y=340)
        self.search_button = ctk.CTkButton(self, text="Buscar", command=self.search, width=120, fg_color='#FFDAA0', text_color='black')
        self.search_button.place(x=480, y=339)
        
        #self.select_button = ctk.CTkButton(self, text="Selecionar", command=get_selected_row, width=120, fg_color='#FFDAA0', text_color='black')
        #self.select_button.place(x=280, y=535)
        
        self.export_button = ctk.CTkButton(self, text="Exportar Para Excel", command=self.export_to_excel, width=120, fg_color='#B99352', text_color='black')
        self.export_button.place(x=420, y=575)
        
        self.about_us_button = ctk.CTkButton(self, text="Acerca", command=self.about_us, width=120, fg_color='#B99352', text_color='black')
        self.about_us_button.place(x=550, y=575)
        
        self.fetch()
        # Adding PlaceHolders
        #self.restart_text()
        
       # Creating Datas to test 
        #data = [
        #    ('01','Eu','Sou','eu@gmael.com','923','932','Tudo e Todas as coisas'),
        #    ('02','I','A m','i@gmael.com','931','913','Everything, Everything')
        #]
        #
        #for item in data:
        #    self.tree.insert("", "end", values=item)

        
        
    def create(self):
        firstname = self.firstname_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        phone1 = self.phone1_entry.get()
        phone2 = self.phone2_entry.get()
        obs = self.obs_entry.get()
        if ((firstname != '' or surname != '') and (phone1 != '' or phone2 !='')):
            #
            self.clear_button['command'] = self.clear
            #
            image_link = self.img
            print(f'\n\nCREATE image_link = {image_link}\n\n')
            create_contact(firstname, surname, email, phone1, phone2, image_link, obs)
            self.fetch()
        else:
            messagebox.showwarning('Atenção','Precisa digitar pelo menos um dos nomes e um número de telefone')
        pass
    def update(self):
        #if (self.id_entry.get() == '' or self.id_entry.get() !=''):
        #    messagebox.showwarning('Atenção',"A opcção 'Actualizar'* ainda não foi finalizada!")
        #    return 0
        id = self.id_entry.get()
        firstname = self.firstname_entry.get()
        surname = self.surname_entry.get()
        email = self.email_entry.get()
        phone1 = self.phone1_entry.get()
        phone2 = self.phone2_entry.get()
        obs = self.obs_entry.get()
        if ((id!='') and ((firstname != '' or surname != '') and (phone1 != '' or phone2 !=''))):
            #
            #image_link = load_image_by_id(self, id)
            image_link = load_image_by_id(self, id)
            print(f'\n\nCREATE image_link = {image_link}\nself.img = {self.img}\n\n')
            self.clear_button['command'] = self.clear
            #
            update_contact(id, firstname, surname, email, phone1, phone2, image_link, obs)
            self.fetch()
        else:
            if (id==''):
                messagebox.showwarning('Atenção','Precisa selecionar um contacto cadastrado.')
            else:
                messagebox.showwarning('Atenção','Precisa digitar pelo menos um dos nomes e um número de telefone')
        pass
    def delete(self):
        id = self.id_entry.get()
        if (id!=''):
            #
            self.clear_button['command'] = self.clear
            #
            delete_contact(id)
            self.fetch()
        else:
            messagebox.showwarning('Atenção','Precisa selecionar um contacto cadastrado.')
        pass
    
    def fetch(self):
        self.clear_list()
        all_contacts = fetch_agenda()
        self.agendados = all_contacts
        for contact in all_contacts:
            self.tree.insert('', tk.END, value=contact)
            
    global agendados
    def search(self):
        search_value = ''
        search_value = self.search_entry.get()
        self.clear_list()
        all_contacts = search_contact(search_value)
        self.agendados = all_contacts
        for contact in all_contacts:
            self.tree.insert('', tk.END, value=contact)
        pass
    
    def export_to_excel(self):
        self.agendados = pd.DataFrame(self.agendados, columns=['ID','Nome','Sobrenome', 'Email', 'Telefone 1', 'Telefone 2', 'Observações'])
        self.agendados.to_excel('Agenda.xlsx')
        messagebox.showinfo('Efectuado', 'Os dados da lista foram anexados a uma tabela no Excel.')
        pass
    
    def about_us(self):
        messagebox.showinfo('Acerca De...', 'Este Software tem como objectivo armazenar informação de contacto.\n\nInformações : Nome, Sobrenome, Email, Telefone 1, Telefone 2, Observações.\n_ Permite Adicionar, Remover, Listar, Buscar e Deletar as informação de um contacto.\n\n_ É possível exportar os dados listados para uma tabela no Excel.\n\n\t            Agenda De Contactos\n\n\t@coppyright J2F AllRightsReserved')
        pass




if __name__== '__main__':
    program = Program()
    program.mainloop()
