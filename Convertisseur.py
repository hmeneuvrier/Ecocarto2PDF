import json
from fpdf import FPDF

# ✅ Nettoyage des caractères spéciaux
def clean_text(text):
    if isinstance(text, str):
        # return text.replace("?", "'").encode('utf-8', 'replace').decode('utf-8')ccc
        return text.replace("?", "'blobbobo'").encode('latin-1', 'replace').decode('latin-1')
    return str(text)

# Dictionnaire de traduction des jours en français
jours_francais = {
    "Mo": "Lundi",
    "Tu": "Mardi",
    "We": "Mercredi",
    "Th": "Jeudi",
    "Fr": "Vendredi",
    "Sa": "Samedi",
    "Su": "Dimanche"
}

# 📄 Classe PDF avec "horaires particuliers"
class PDFUpdated(FPDF):
    def __init__(self):
        super().__init__()
        self.set_font('Arial', '', 12)

    def header(self):
        if self.page_no() == 1:
            self.image('logo.png', 68, 25, 80)
            self.ln(117)

        if self.page_no() > 1:
            self.set_font('Arial', 'I', 10)
            self.cell(0, 10, '', 0, 0, 'C')
            self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Arial', 'B', 14)
        self.set_fill_color(84, 177, 95)
        self.cell(0, 10, clean_text(title), 0, 1, 'L', True)
        self.ln(15)

    def chapter_body(self, body):
        self.set_font('Arial', '', 12)
        self.multi_cell(0, 10, clean_text(body))
        self.ln()

    def add_entity(self, entity):
        name = entity.get('name', 'Nom inconnu')
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, clean_text(name), ln=True)
        self.set_font('Arial', '', 11)

        details = [
            f"Adresse : {entity.get('address', {}).get('customFormatedAddress', 'Non renseignée')}",
            f"Téléphone : {entity.get('telephone', 'Non renseigné')}",
            f"Email : {entity.get('email', 'Non renseigné')}",
            f"Site Web : {entity.get('url', 'Non renseigné')}",
            f"Détails : {entity.get('details', 'Non renseigné')}"
        ]

        # 📅 Horaires d'ouverture
        open_hours = entity.get('openHours', {})
        if open_hours:
            self.cell(0, 10, "Horaires d'ouverture :", ln=True)
            self.set_font('Arial', '', 10)
            for day, hour in open_hours.items():
                jour_fr = jours_francais.get(day, day)
                self.multi_cell(0, 8, f"{jour_fr}: {hour}")
            self.ln(3)

        # 🕑 Horaires particuliers
        horaires_particuliers = entity.get('detailshoraires', None)
        if horaires_particuliers:
            self.set_font('Arial', 'B', 11)
            self.cell(0, 10, "Horaires particuliers :", ln=True)
            self.set_font('Arial', '', 10)
            self.multi_cell(0, 8, clean_text(horaires_particuliers))
            self.ln(3)

        for detail in details:
            self.multi_cell(0, 8, clean_text(detail))
        self.ln(5)

        if self.get_y() > 260:
            self.add_page()


# 📚 Chargement du fichier JSON
with open('elements.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 🖨️ Création du PDF final
pdf = PDFUpdated()
pdf.set_auto_page_break(auto=True, margin=15)
pdf.add_page()

# ✍️ Introduction
intro = ("Ce document regroupe les informations des ressourceries, ateliers de création, producteurs locaux et d'autres situés autour de Saint mars du Désert. Les données proviennent d'une cartographie réalisée par le Collectif Eco-citoyen marsien qui contient l'enrièrté des informations trier et placer sur une carte (n'hésitez pas à aller consulter sur le site du Tiers lieu : https://tierslieumarsien.fr/le-collectif-eco-citoyen/). Cependant afin d'améliorer la lisibilité et la consultation de ces informations, nous avons aussi centralisé toutes les données dans ce document unique. Chaque lieu est décrit de manière présice avec le plus d'informations possibles. Cette initiative s'inscrit dans notre engagement pour soutenir des actions locales qui constituent une économie circulaire. Nous espérons que ce guide vous aidera à trouver facilement les ressources disponibles près de chez vous. N'hésitez pas à consulter la cartographie en ligne pour plus de détails.")

pdf.chapter_title("Tiers lieu marsien : Collectif eco-citoyen")
pdf.chapter_body(intro)

# 📋 Ajout des entités
pdf.chapter_title("Catalogue des ressourceries et producteurs locaux et bien plus....")
for entity in data.get("data", []):
    pdf.add_entity(entity)

# 💾 Sauvegarde du PDF final
pdf.output('Données de la Carto - Complet.pdf')

print("✅ PDF généré avec succès : 'Données de la Carto - Complet.pdf'")
