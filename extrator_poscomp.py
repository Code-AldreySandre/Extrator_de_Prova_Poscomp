import fitz
import os
import re
import json
from typing import List, Dict

class Questao:
    def __init__(self, numero: int, enunciado: str, alternativas: Dict[str, str], page_num: int):
        self.numero = numero
        self.enunciado = enunciado
        self.alternativas = alternativas
        self.page_num = page_num
        self.images = []
        self.has_images = False
        self.subject = None
        self.MAT = False
        self.FumComp = False
        self.TecComp = False

    def to_dict(self):
        return {
            'numero': self.numero,
            'enunciado': self.enunciado,
            'alternativas': self.alternativas,
            'page_num': self.page_num,
            'images': self.images,
            'has_images': self.has_images,
            'subject': self.subject,
            'MAT': self.MAT,
            'FumComp': self.FumComp,
            'TecComp': self.TecComp
        }

class PoscompExtractor:
    def __init__(self, pdf_path: str, prova_nome: str, output_img_folder: str = 'imgs'):
        self.pdf_path = pdf_path
        self.prova_nome = prova_nome  # ex: "2022"
        self.output_img_folder = output_img_folder
        os.makedirs(self.output_img_folder, exist_ok=True)
        self.doc = fitz.open(pdf_path)
        self.texto_paginas = [pagina.get_text("text") for pagina in self.doc]

    # Definição dos ninchos no qual a  prova da poscomp é divida
    def _define_nicho(self, numero_questao: int):
        if 1 <= numero_questao <= 20:
            return 'MAT'
        elif 21 <= numero_questao <= 50:
            return 'FumComp'
        elif 51 <= numero_questao <= 70:
            return 'TecComp'
        else:
            return None

    def extrair_questoes_com_paginas(self) -> List[Questao]:
        questoes = []
        padrao = re.compile(r"(QUESTÃO\s(\d{2})\s+–\s+)(.*?)(?=QUESTÃO\s\d{2}\s+–|$)", re.DOTALL)

        for i, texto in enumerate(self.texto_paginas):
            pagina_num = i + 1
            matches = padrao.findall(texto)
            for full_match, num_str, texto_questao in matches:
                numero = int(num_str)

                # Separarando o enunciado e as  alternativas
                partes = re.split(r"\n[A-E]\)", texto_questao)
                enunciado = partes[0].strip() if partes else texto_questao.strip()

                alternativas = {}
                padrao_alt = re.compile(r"\n([A-E])\)\s*(.*?)\s*(?=\n[A-E]\)|$)", re.DOTALL)
                for letra, texto_alt in padrao_alt.findall(texto_questao):
                    alternativas[letra] = texto_alt.strip()

                questao = Questao(numero, enunciado, alternativas, pagina_num)

                nicho = self._define_nicho(numero)
                questao.subject = nicho
                if nicho == 'MAT':
                    questao.MAT = True
                elif nicho == 'FumComp':
                    questao.FumComp = True
                elif nicho == 'TecComp':
                    questao.TecComp = True

                questoes.append(questao)
        return questoes

    def extrair_e_salvar_imagens(self, questoes: List[Questao]):

        # mapa: página -> questões daquela página 
        questoes_por_pagina = {}
        for q in questoes:
            questoes_por_pagina.setdefault(q.page_num, []).append(q)

        for i, pagina in enumerate(self.doc):
            pagina_num = i + 1
            imagens = pagina.get_images(full=True)
            if imagens:
                for img_index, img in enumerate(imagens, start=1):
                    xref = img[0]
                    base_im = self.doc.extract_image(xref)
                    image_bytes = base_im["image"]
                    image_ext = base_im["ext"]

                    # Se não tiver questões na página, não faz sentido salvar imagem né
                    if pagina_num not in questoes_por_pagina:
                        continue

                    # Assumindo  que a imagem pertence a todas as questões da página
                    for questao in questoes_por_pagina[pagina_num]:
                        img_name = f"{self.prova_nome}_questao_{questao.numero:02d}_img_{img_index}.{image_ext}"
                        img_path = os.path.join(self.output_img_folder, img_name)
                        with open(img_path, "wb") as img_file:
                            img_file.write(image_bytes)
                        questao.images.append(img_name)
                        questao.has_images = True

    def salvar_questoes_json(self, questoes: List[Questao], output_json="questoes.json"):
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump([q.to_dict() for q in questoes], f, indent=4, ensure_ascii=False)
        print(f"[+] Questões salvas no arquivo {output_json}")

if __name__ == "__main__":
    prova_nome = "2022"  # nesse aqui, ajuste o nome pra prefixar as imagens da prova
    pdf_file = f"Provas/{prova_nome}/caderno_{prova_nome}.pdf"  # Aqui, ajuste o caminho

    extrator = PoscompExtractor(pdf_file, prova_nome)
    questoes = extrator.extrair_questoes_com_paginas()
    extrator.extrair_e_salvar_imagens(questoes)
    extrator.salvar_questoes_json(questoes, f"questoes_{prova_nome}.json")