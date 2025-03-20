import tkinter as tk
from tkinter import messagebox, scrolledtext, ttk
from datetime import datetime
from openpyxl import Workbook
import threading

# Lista para armazenar os chamados
chamados = []

def atualizar_data_hora():
    while True:
        data_atual = datetime.now().strftime("%d/%m/%Y")
        hora_atual = datetime.now().strftime("%H:%M:%S")
        label_data.config(text=f"Data: {data_atual}")
        label_hora.config(text=f"Hora: {hora_atual}")
        root.update()
        threading.Event().wait(1)  # Atualiza a cada 1 segundo

def registrar_chamado():
    data = datetime.now().strftime("%d/%m/%Y")
    
    # Verifica se o checkbox está marcado (usar hora atual)
    if var_usar_hora_atual.get():
        horario = datetime.now().strftime("%H:%M:%S")
    else:
        horario = entry_hora_manual.get()
        if not horario:
            messagebox.showwarning("Campo Vazio", "Por favor, insira a hora manualmente.")
            return

    nome_estagiario = entry_estagiario.get()
    unidade = combo_unidade.get()
    sala = entry_sala.get()
    nome_professor = entry_professor.get()
    motivo = entry_motivo.get()
    descricao = text_descricao.get("1.0", tk.END).strip()

    if not all([nome_estagiario, unidade, sala, nome_professor, motivo, descricao]):
        messagebox.showwarning("Campos Vazios", "Por favor, preencha todos os campos.")
        return

    # Criando um dicionário com os dados do chamado
    chamado = {
        "Data": data,
        "Horário": horario,
        "Estagiário": nome_estagiario,
        "Unidade": unidade,
        "Sala": sala,
        "Professor": nome_professor,
        "Motivo": motivo,
        "Descrição": descricao
    }

    # Adicionando o chamado à lista
    chamados.append(chamado)
    messagebox.showinfo("Sucesso", "Chamado registrado com sucesso!")
    limpar_campos()

def limpar_campos():
    entry_estagiario.delete(0, tk.END)
    entry_sala.delete(0, tk.END)
    entry_professor.delete(0, tk.END)
    entry_motivo.delete(0, tk.END)
    text_descricao.delete("1.0", tk.END)
    entry_hora_manual.delete(0, tk.END)

def gerar_relatorio():
    if not chamados:
        messagebox.showinfo("Sem Chamados", "Nenhum chamado registrado.")
        return

    # Criando um arquivo Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Chamados"

    # Adicionando cabeçalhos
    cabecalhos = ["Data", "Horário", "Estagiário", "Unidade", "Sala", "Professor", "Motivo", "Descrição"]
    ws.append(cabecalhos)

    # Adicionando os chamados
    for chamado in chamados:
        linha = [
            chamado["Data"],
            chamado["Horário"],
            chamado["Estagiário"],
            chamado["Unidade"],
            chamado["Sala"],
            chamado["Professor"],
            chamado["Motivo"],
            chamado["Descrição"]
        ]
        ws.append(linha)

    # Salvando o arquivo
    data_atual = datetime.now().strftime("%Y-%m-%d")
    nome_arquivo = f"relatorio_chamados_{data_atual}.xlsx"
    wb.save(nome_arquivo)
    messagebox.showinfo("Relatório Salvo", f"Relatório salvo em '{nome_arquivo}'")

# Criando a janela principal
root = tk.Tk()
root.title("Registro de Chamados - Unifacef")

# Labels para data e hora
label_data = tk.Label(root, text="Data: ", font=("Arial", 10))
label_data.grid(row=0, column=0, padx=10, pady=5, sticky="w")

label_hora = tk.Label(root, text="Hora: ", font=("Arial", 10))
label_hora.grid(row=0, column=1, padx=10, pady=5, sticky="w")

# Iniciando a atualização da data e hora em tempo real
threading.Thread(target=atualizar_data_hora, daemon=True).start()

# Checkbox para usar hora atual
var_usar_hora_atual = tk.BooleanVar(value=True)
checkbox_hora_atual = tk.Checkbutton(
    root, text="Usar hora atual", variable=var_usar_hora_atual,
    command=lambda: entry_hora_manual.config(state=tk.DISABLED if var_usar_hora_atual.get() else tk.NORMAL)
)
checkbox_hora_atual.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# Campo de entrada para hora manual
tk.Label(root, text="Hora Manual (HH:MM:SS):").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_hora_manual = tk.Entry(root, state=tk.DISABLED)
entry_hora_manual.grid(row=2, column=1, padx=10, pady=5)

# Campos de entrada
tk.Label(root, text="Nome do Estagiário:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
entry_estagiario = tk.Entry(root)
entry_estagiario.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Unidade (1, 2 ou 3):").grid(row=4, column=0, padx=10, pady=5, sticky="e")
combo_unidade = ttk.Combobox(root, values=["1", "2", "3"], state="readonly")
combo_unidade.grid(row=4, column=1, padx=10, pady=5)
combo_unidade.current(0)

tk.Label(root, text="Número da Sala:").grid(row=5, column=0, padx=10, pady=5, sticky="e")
entry_sala = tk.Entry(root)
entry_sala.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Nome do Professor:").grid(row=6, column=0, padx=10, pady=5, sticky="e")
entry_professor = tk.Entry(root)
entry_professor.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="Motivo da Chamada:").grid(row=7, column=0, padx=10, pady=5, sticky="e")
entry_motivo = tk.Entry(root)
entry_motivo.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="Descrição do que foi feito:").grid(row=8, column=0, padx=10, pady=5, sticky="e")
text_descricao = tk.Text(root, width=40, height=5)
text_descricao.grid(row=8, column=1, padx=10, pady=5)

# Botões
tk.Button(root, text="Registrar Chamado", command=registrar_chamado).grid(row=9, column=0, columnspan=2, pady=10)
tk.Button(root, text="Gerar Relatório", command=gerar_relatorio).grid(row=10, column=0, columnspan=2, pady=10)

# Iniciando o loop principal da interface gráfica
root.mainloop()