# 🧠 Projeto DiagPlus – Chatbot de Diagnóstico por Sintomas

O **DiagPlus** é um sistema interativo que simula um chatbot de diagnóstico médico baseado em sintomas falados ou digitados pelo usuário. Ele permite que o usuário receba sugestões de possíveis doenças a partir de uma base local de sintomas e diagnósticos, mantendo também o histórico de atendimentos.

---

## ✅ O que o sistema faz

1. **Cadastro e login de usuários**  
   Cada usuário pode se registrar e acessar seu ambiente individual. O sistema armazena senhas com segurança (hash SHA-256) e vincula cada atendimento a um usuário específico.

2. **Entrada de sintomas via voz ou texto**  
   Após o login, o usuário pode:
   - Falar seus sintomas usando o microfone;
   - Ou digitar os sintomas manualmente caso prefira.

3. **Diagnóstico automatizado**  
   O sistema compara os sintomas relatados com uma base de dados contendo:
   - Mais de 20 doenças reais;
   - Mais de 50 sintomas diferentes;
   - Relacionamentos bem definidos entre doenças e seus sintomas característicos.

4. **Sugestão de diagnóstico com nível de confiança**  
   A resposta apresentada ao usuário inclui:
   - O nome da doença mais compatível;
   - A lista de sintomas reconhecidos;
   - Um índice de confiança calculado com base na correspondência de sintomas.

5. **Histórico de atendimentos**  
   Cada interação é registrada no banco de dados, permitindo ao usuário consultar:
   - Data do atendimento;
   - Diagnóstico recebido;
   - Sintomas que levaram àquele resultado.

---

## 🗂 Como o sistema foi desenvolvido

- **Linguagem**: Python 3  
- **Interface gráfica**: Tkinter  
- **Reconhecimento de voz**: Google Speech Recognition (via `speech_recognition`)  
- **Banco de dados local**: SQLite, gerenciado pelo DBeaver  
- **Organização modular**:
  - `banco_dados.py`: conexão e operações no banco SQLite  
  - `autenticacao.py`: registro e login de usuários  
  - `voz.py`: captura e transcrição de fala  
  - `diagnostico.py`: vetorização de sintomas e lógica de comparação  
  - `gui.py`: toda a interface e controle de navegação  

---

## 📌 Observações finais

- O banco de dados é totalmente local e já vem populado com dados coerentes para testes realistas.
- A identificação de sintomas é feita por simples busca textual – o projeto é didático e pode ser facilmente expandido para usar NLP ou IA.
- A interface prioriza acessibilidade e simplicidade, permitindo uso básico mesmo por usuários leigos.
