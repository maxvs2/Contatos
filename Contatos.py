import customtkinter as ctk
from supabase import create_client, Client
from tkinter import messagebox

# Dados do Projeto (api key)
url = "" # APAGADO POR SEGURANÇA  
key = "" # APAGADO POR SEGURANÇA
supabase: Client = create_client(url, key)


# Inicializar a interface
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("📇 Gerenciador de Contatos")
app.geometry("600x500")
 
# ==== Funções ====

# Função: Listar todos os contatos
def listar_contatos():
    resposta = supabase.table("contatos").select("*").execute()
    contatos_listbox.delete("1.0", "end")  # <- CORRIGIDO

    if resposta.data:
        for contato in resposta.data:
            contatos_listbox.insert("end", f"ID: {contato['id']}\n")
            contatos_listbox.insert("end", f"Nome: {contato['nome']}\n")
            contatos_listbox.insert("end", f"Número: {contato['numero']}\n\n")
    else:
        contatos_listbox.insert("end", "Nenhum contato cadastrado.")

# Função: Adicionar novo contato
def adicionar_contato():
    nome = nome_entry.get()
    try:
        numero = int(numero_entry.get())
    except ValueError:
        messagebox.showerror("Erro", "Número inválido.")
        return

    if nome:
        resposta = supabase.table("contatos").insert({"nome": nome, "numero": numero}).execute()
        messagebox.showinfo("Sucesso", "Contato adicionado!")
        listar_contatos()
        nome_entry.delete(0, "end")
        numero_entry.delete(0, "end")
    else:
        messagebox.showwarning("Atenção", "Preencha todos os campos.")

# Função: Atualizar número de contato
def deletar_contato():
    try:
        id_ = int(deletar_entry.get())
        resposta = supabase.table("contatos").delete().eq("id", id_).execute()
        messagebox.showinfo("Sucesso", f"Contato ID {id_} deletado.")
        listar_contatos()
    except ValueError:
        messagebox.showerror("Erro", "ID inválido.")

# Função: Deletar contato
def atualizar_contato():
    try:
        id_ = int(atualizar_id_entry.get())
        novo_numero = int(atualizar_numero_entry.get())
        resposta = supabase.table("contatos").update({"numero": novo_numero}).eq("id", id_).execute()
        messagebox.showinfo("Atualizado", "Número atualizado com sucesso.")
        listar_contatos()
    except ValueError:
        messagebox.showerror("Erro", "Preencha corretamente os campos.")

"""
# === Menu Interface ===
while True:
    print("\n ==== Menu de Contatos ====")
    print("1 - Listar todos os contatos")
    print("2 - Buscar contato por ID")
    print("3 - Adicionar contato")
    print("4 - Atualizar número do contato")
    print("5 - Deletar contato")
    print("0 - Encerrar programa")
    
    opcao = input("Escolha uma opção: ")  
    
    if opcao == "1":
        listar_contatos()
    elif opcao == "2":
        busca_por_id()
    elif opcao == "3":
        adicionar_nome()
    elif opcao == "4":
        atualizar_nome()
    elif opcao == "5":
        deletar_nome()
    elif opcao == "0":
        print("Programa encerrado. 👋")
        break
    else:
        print("Opção inválida, tente novamente.")
"""

# ==== Layout ====

# Frame de entrada
input_frame = ctk.CTkFrame(app)
input_frame.pack(pady=10, fill="x", padx=20)

nome_entry = ctk.CTkEntry(input_frame, placeholder_text="Nome")
nome_entry.pack(side="left", padx=10, fill="x", expand=True)

numero_entry = ctk.CTkEntry(input_frame, placeholder_text="Número")
numero_entry.pack(side="left", padx=10, fill="x", expand=True)

add_button = ctk.CTkButton(input_frame, text="➕ Adicionar", command=adicionar_contato)
add_button.pack(side="left", padx=10)

# Lista de contatos
contatos_listbox = ctk.CTkTextbox(app, height=200)
contatos_listbox.pack(pady=10, padx=20, fill="both", expand=True)

# Frame atualizar
atualizar_frame = ctk.CTkFrame(app)
atualizar_frame.pack(pady=5, padx=20, fill="x")

atualizar_id_entry = ctk.CTkEntry(atualizar_frame, placeholder_text="ID para atualizar")
atualizar_id_entry.pack(side="left", padx=10)

atualizar_numero_entry = ctk.CTkEntry(atualizar_frame, placeholder_text="Novo número")
atualizar_numero_entry.pack(side="left", padx=10)

atualizar_button = ctk.CTkButton(atualizar_frame, text="✏️ Atualizar", command=atualizar_contato)
atualizar_button.pack(side="left", padx=10)

# Frame deletar
deletar_frame = ctk.CTkFrame(app)
deletar_frame.pack(pady=5, padx=20, fill="x")

deletar_entry = ctk.CTkEntry(deletar_frame, placeholder_text="ID para deletar")
deletar_entry.pack(side="left", padx=10)

deletar_button = ctk.CTkButton(deletar_frame, text="🗑️ Deletar", command=deletar_contato)
deletar_button.pack(side="left", padx=10)

# Botão atualizar lista
refresh_button = ctk.CTkButton(app, text="🔄 Atualizar Lista", command=listar_contatos)
refresh_button.pack(pady=10)

# Carregar dados na inicialização
listar_contatos()

# Executar a interface
app.mainloop()