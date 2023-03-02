import os
import re
import sys
from pandas_ods_reader import read_ods

EXTENSIONS = [".csv", ".ods"]

def sql_quote(dado: any) -> str:
   return "'" + num_to_str(dado).strip() + "'"   

def num_to_str(dado: any) -> str:
   if dado == None:
      return "XXXXXXXXX"
   if type(dado) != str:
      dado = int(dado)
      dado = str(dado)
   if not dado.isdigit():
      return "XXXXXXXXX"
   return dado

def normalize_cpf(dado:str) -> str:
   if len(dado.strip()) < 11: 
      return "'XXXXXXXXXXX'"
   dado = dado.replace(" ", "/")
   dado = re.sub(r"[a-zA-Z]", "", dado)
   dado = re.sub(r"\D", "','", dado)
   dado = "'" + dado + "'"
   return dado

def from_folder(path: str) -> None:
   for file in os.listdir(path):
      from_file(os.path.join(path, file))
   return

def sql_path(path: str) -> str:
   new_file,_ = os.path.splitext(os.path.basename(path))
   new_file += ".sql"
   return new_file

def from_file(path: str) -> None:
   dt = read_ods(path)
   new_path = sql_path(path)
   with open(new_path, 'w') as f:
      for telefone, cadastro in zip(dt['Telefone'], dt['Removertelefonenestecadastro']):
         f.write(f"UPDATE CONTATOS SET ALTERA = To_Char(SYSDATE, 'DD/MM/YYYY'), DATA_A = To_Char(SYSDATE, 'DD/MM/YYYY'), DDD_CEL = NULL, CELULAR = NULL WHERE CPF IN ( {normalize_cpf(num_to_str(cadastro))} ) AND CELULAR = {sql_quote(telefone)}; \n")
         f.write(f"UPDATE CONTATOS SET ALTERA = To_Char(SYSDATE, 'DD/MM/YYYY'), DATA_A = To_Char(SYSDATE, 'DD/MM/YYYY'), DDD_CEL2 = NULL, CELULAR2 = NULL WHERE CPF IN ( {normalize_cpf(num_to_str(cadastro))} ) AND CELULAR2 = {sql_quote(telefone)}; \n")

def main():
   if sys.argv[1] == '--file':
      _, ext = os.path.splitext(sys.argv[2])
      if ext not in EXTENSIONS:
         print(f"extensoes validas => {EXTENSIONS}")

      from_file(sys.argv[2])
      
   elif len(sys.argv) > 2:
      print("Forneça o path para a pasta ou => --file [path para o arquivo]")
   else:
      from_folder(sys.argv[1])


if __name__ == '__main__':
   main()