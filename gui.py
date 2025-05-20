import tkinter as tk
from tkinter import messagebox
from autenticacao import registrar, efetuar_login
from voz import ouvir_sintomas
from diagnostico import texto_para_vetor, comparar_e_diagnosticar
from banco_dados import executar_query, executar_comando
from datetime import datetime

class Aplicativo(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("DiagPlus - Diagnóstico por Sintomas")
        self.geometry("400x250")
        self.usuario_id = None
        self.exibir_tela_login()

    def limpar_tela(self):
        for widget in self.winfo_children():
            widget.destroy()

    def exibir_tela_login(self):
        self.limpar_tela()
        tk.Label(self, text="Usuário").pack()
        campo_usuario = tk.Entry(self)
        campo_usuario.pack()
        tk.Label(self, text="Senha").pack()
        campo_senha = tk.Entry(self, show="*")
        campo_senha.pack()

        tk.Button(self, text="Entrar", command=lambda: self.login(campo_usuario.get(), campo_senha.get())).pack(pady=5)
        tk.Button(self, text="Registrar", command=lambda: self.registrar(campo_usuario.get(), campo_senha.get())).pack()

    def registrar(self, nome, senha):
        if not nome or not senha:
            messagebox.showwarning("Atenção", "Preencha usuário e senha.")
            return
        if registrar(nome, senha):
            messagebox.showinfo("Sucesso", "Usuário registrado com sucesso.")
        else:
            messagebox.showerror("Erro", "Nome de usuário já existe.")

    def login(self, nome, senha):
        uid = efetuar_login(nome, senha)
        if uid:
            self.usuario_id = uid
            self.exibir_tela_principal()
        else:
            messagebox.showerror("Erro", "Usuário ou senha inválidos.")

    def exibir_tela_principal(self):
        self.limpar_tela()
        tk.Label(self, text="Bem-vindo!", font=("Arial", 14)).pack(pady=10)
        tk.Button(self, text="Falar sintomas", command=self.capturar_diagnosticar).pack(pady=10)
        tk.Button(self, text="Digitar sintomas", command=self.digitar_sintomas).pack(pady=10)
        tk.Button(self, text="Ver histórico", command=self.exibir_historico).pack(pady=10)
        tk.Button(self, text="Sair", command=self.exibir_tela_login).pack(pady=10)

    def capturar_diagnosticar(self):
        texto = ouvir_sintomas()
        if not texto:
            messagebox.showwarning("Aviso", "Nenhum áudio reconhecido.")
            return

        self.processar_diagnostico(texto)

    def digitar_sintomas(self):
        janela = tk.Toplevel(self)
        janela.title("Digitar sintomas")
        janela.geometry("400x200")

        tk.Label(janela, text="Descreva seus sintomas:").pack(pady=5)
        entrada = tk.Entry(janela, width=50)
        entrada.pack(pady=5)

        def ao_confirmar():
            texto = entrada.get().lower().strip()
            if texto:
                self.processar_diagnostico(texto)
                janela.destroy()
            else:
                messagebox.showwarning("Aviso", "Informe ao menos um sintoma.")

        tk.Button(janela, text="Confirmar", command=ao_confirmar).pack(pady=10)

    def processar_diagnostico(self, texto):
        vetor = texto_para_vetor(texto)
        doenca_id = comparar_e_diagnosticar(vetor)

        if doenca_id:
            nome = next(executar_query("SELECT nome FROM doencas WHERE id = ?", (doenca_id,)))[0]
            sintomas_nomes = [s[0] for s in executar_query(
                f"SELECT descricao FROM sintomas WHERE id IN ({','.join(str(s) for s, v in vetor.items() if v == 1)})"
            )]
            lista_sintomas = ", ".join(sintomas_nomes)
            total_sintomas = len([v for v in vetor.values() if v == 1])
            total_doenca = len(list(executar_query("SELECT sintoma_id FROM doenca_sintoma WHERE doenca_id = ?", (doenca_id,))))
            score = total_sintomas / total_doenca if total_doenca else 0
            messagebox.showinfo("Diagnóstico", f"Sintomas: {lista_sintomas}\n\nDiagnóstico sugerido: {nome}\nConfiança: {score*100:.1f}%")

            sintomas_str = ",".join(str(s) for s, v in vetor.items() if v == 1)
            executar_comando(
                "INSERT INTO historico(usuario_id, sintomas_reconhecidos, diagnostico_id, data) VALUES (?, ?, ?, ?)",
                (self.usuario_id, sintomas_str, doenca_id, datetime.now().date().isoformat())
            )
        else:
            messagebox.showinfo("Diagnóstico", f"Sintomas: {texto}\n\nNão foi possível determinar um diagnóstico.")

    def exibir_historico(self):
        janela = tk.Toplevel(self)
        janela.title("Histórico de Atendimentos")
        janela.geometry("500x400")

        tk.Label(janela, text="Seus atendimentos:", font=("Arial", 12, "bold")).pack(pady=10)

        historico = list(executar_query("""
            SELECT h.data, d.nome, h.sintomas_reconhecidos
            FROM historico h
            JOIN doencas d ON h.diagnostico_id = d.id
            WHERE h.usuario_id = ?
            ORDER BY h.data DESC
        """, (self.usuario_id,)))

        if not historico:
            tk.Label(janela, text="Nenhum atendimento encontrado.").pack()
            return

        frame = tk.Frame(janela)
        frame.pack(fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        lista = tk.Listbox(frame, yscrollcommand=scrollbar.set, width=70)
        lista.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=lista.yview)

        for data, nome_doenca, sintomas in historico:
            ids = sintomas.split(',') if sintomas else []
            nomes = [s[0] for s in executar_query(
                f"SELECT descricao FROM sintomas WHERE id IN ({','.join(ids)})"
            )] if ids else []
            lista.insert("end", f"{data} - {nome_doenca}")
            lista.insert("end", f"  Sintomas: {', '.join(nomes)}")
            lista.insert("end", "-" * 60)

if __name__ == '__main__':
    app = Aplicativo()
    app.mainloop()
