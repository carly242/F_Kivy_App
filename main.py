from kivy.config import Config
Config.set('graphics', 'width', '400')  # Largeur de la fenêtre
Config.set('graphics', 'height', '640')  # Hauteur de la fenêtre

import random
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import Screen
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.dialog import MDDialog
from kivy.uix.image import Image
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.popup import Popup


class GuessRiddleApp(MDApp):
    def build(self):
        # Initialisation du jeu et des niveaux
        self.level = 1  # Commence au niveau 1
        self.devinettes_resolues = 0
        self.devinettes_par_niveau = 25
        self.used_riddles = set()  # Ensemble pour stocker les devinettes utilisées
        self.current_riddle, self.current_answer = self.get_random_riddle()
        self.score = 0
        self.temps_restants = 600  # 20 minutes pour le niveau 1

        # Créer l'écran principal
        screen = Screen()

        # Ajouter l'image au-dessus du score
        logo_image = Image(
            source="deviner.jpg",  # Remplace par le nom de ton image
            size_hint=(0.2, 0.2),
            pos_hint={"center_x": 0.2, "center_y": 0.95}
        )
        screen.add_widget(logo_image)

        # Affichage du score
        self.score_label = MDLabel(
            text=f"Score: {self.score} | Niveau: {self.level}",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.9}
        )

        screen.add_widget(self.score_label)
        # Affichage du score et du niveau
        

        # Affichage de la devinette
        self.riddle_label = MDLabel(
            text=f"Devinette : {self.current_riddle}",
            halign="center",
            theme_text_color="Primary",
            font_style="H5",
            pos_hint={"center_x": 0.5, "center_y": 0.7}
        )
        screen.add_widget(self.riddle_label)

        # Champ de saisie pour la réponse de l'utilisateur
        self.input_field = MDTextField(
            hint_text="Entrez votre réponse",
            size_hint_x=0.8,
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            mode="rectangle"
        )
        screen.add_widget(self.input_field)

        # Bouton pour valider la réponse
        guess_button = MDRaisedButton(
            text="Valider",
            pos_hint={"center_x": 0.5, "center_y": 0.4},
            on_release=self.check_guess
        )
        screen.add_widget(guess_button)

        # Bouton pour réinitialiser le jeu
        reset_button = MDRaisedButton(
            text="Réinitialiser",
            pos_hint={"center_x": 0.5, "center_y": 0.3},
            on_release=lambda x: self.reset_game()
        )
        screen.add_widget(reset_button)

        # Bouton Pause
        pause_button = MDRaisedButton(
            text="Pause",
            pos_hint={"center_x": 0.5, "center_y": 0.2},
            on_release=self.pause_game
        )
        screen.add_widget(pause_button)

        # Label du timer
        self.timer_label = MDLabel(
            text="Temps restant: 20:00",
            halign="center",
            pos_hint={"center_x": 0.5, "center_y": 0.1}
        )
        screen.add_widget(self.timer_label)

        # Démarrer le timer
        self.start_timer()

        return screen

    def get_random_riddle(self):
        """Renvoie une devinette aléatoire pour le niveau actuel."""
        level_1_riddles = [
            ("Quel est l'animal qui fait meuh ?", "vache"),
            ("Qu'est-ce qui doit être cassé avant qu'on l'utilise ?", "oeuf"),
            ("Je ne peux pas marcher mais j'ai pourtant un dos et quatre pieds. Qui suis-je?", "chaise"),
            ("Qu'est-ce qui est toujours devant vous mais que vous ne pouvez jamais atteindre?", "avenir"),
            ("Je suis parfois blanc et je peux couvrir le sol. Mais attention, je fond au soleil. Qui suis-je?", "neige"),
            ("Qu'est-ce qui a un cou mais pas de tête ?", "bouteille"),
            ("Qu'est-ce qui monte et descend sans bouger ?", "escalier"),
            ("Qu'est-ce qui peut être cassé sans être touché ?", "promesse"),
            ("Qu'est-ce qui a des dents mais ne mord pas ?", "peigne"),
            ("Qu'est-ce qui a des feuilles mais n'est pas un arbre ?", "livre"),
            ("Quel est l'endroit où la nuit tombe et ne se relève jamais ?", "sol"),
            ("Qu'est-ce qui est blanc quand il est sale et noir quand il est propre ?", "tableau blanc"),
            ("Qu'est-ce qui est plein de trous mais qui peut contenir de l'eau ?", "éponge"),
            ("Qu'est-ce qui peut être entendu mais jamais vu ?", "son"),
            ("Je suis léger comme une plume, mais même le plus fort des hommes ne peut me porter longtemps. Qui suis-je ?", "souffle"),
            ("Plus je suis vieux, plus je suis précieux. Qui suis-je ?", "vin"),
            ("Je suis souvent servi à la table, mais je ne peux pas être mangé. Qui suis-je ?", "plat"),
            ("Je suis grand quand je suis jeune et petit quand je suis vieux, qui suis-je ?", "bougie"),
            ("On ne peut pas me tenir tant qu'on ne m'a pas donné, que suis-je ?", "parole"),
            ("Qu'est-ce qui augmente mais ne diminue jamais ?", "âge"),
            ("Qu'est-ce qu'on peut attraper mais jamais lancer ?", "rhume"),
            ("Qu'est-ce qui a quatre doigts et un pouce mais n'est pas vivant ?","gant"),
            ("Qu'est-ce qui ne peut pas parler mais répond quand on lui parle ?", "écho"),
            ("Si vous m'avez, vous voudrez me partager, mais si vous me partagez je n'existe plus, que suis-je ?", "secret"),
            ("Qu'est-ce qui est léger comme une plume mais que même la personne la plus forte ne peut retenir pendant 10 minutes ?", "respiration"),
            ("Quelle invention permet de regarder à travers les murs ?", "fenêtres"),

            # Ajoute d'autres devinettes de niveau 1 ici...
        ]
        level_2_riddles = [
            ("Je suis là quand il fait nuit et je disparais au lever du jour. Qui suis-je?", "étoile"),
            ("Je suis une question sans réponse. Plus tu me cherches, plus je m'éloigne. Qui suis-je?", "mystère"),
            ("Plus je suis grand, moins on me voit. Qui suis-je?", "obscurité"),
            ("Les parents de Pierre ont trois enfants, Paul et Bill : quel est le nom du troisième enfant ?", "pierre"),
            ("Si vous doublez la deuxième personne dans une course, à quelle place vous trouvez-vous ?", "deuxième"),
            ("Je vous appartiens mais les autres personnes m'utilisent plus que vous, que suis-je ?", "mon prénom"),
            ("Qu'est qui se trouve une fois dans une minute, deux fois dans un moment mais jamais dans une heure ?", "m"),
            ("Qu'est-ce qui est à la fin d'un arc en ciel ?", "l"),
            ("Quel établissement possède le plus d'histoires ?", "bibliothèque"),
            ("L'homme qui m'a inventé n'en a plus besoin, l'homme qui m'achète n'en veut pas, l'homme qui en a besoin ne le sait pas, qui-suis je ?", "cercueil"),
            ("Qu'est-ce qui est plus grand que la Tour Eiffel mais beaucoup moins lourd ?", "son ombre"),
            ("Quel mot contient une lettre ?", "enveloppe"),
            ("Combien peut-on mettre de gouttes d'eau dans un verre vide ?", "une"),
            ("Qu'est-ce qu'on trouve au milieu de Toronto ?", "O"),
            ("Je suis le commencement de tout et la fin de tout, que suis-je ?", "T"),
            ("Plus on en fait, plus on en laisse derrière nous. Qu'est-ce que c'est ?", "traces de pas"),
            ("On peut me fabriquer, m'échanger, m'économiser et me dépenser, qui suis-je ?", "argent"),
            ("Qu'est-ce qui traverse les villes et les champs mais ne bouge jamais ?", "route"),
            ("Quand je mange je grossis, quand je bois je meurs. Qui suis-je ?", "feu"),
            ("Je suis mieux que Dieu et pire que le Diable, les riches en ont besoin et les pauvres en ont, si on me mange on meurt. Que suis-je ?", "rien"),
            ("Je suis facile à soulever mais dur à lancer, que suis-je ?", "plume"),
            ("J'ai deux aiguilles mais je ne pique jamais, que suis-je ?", "montre"),
            ("Qu'est-ce qui rentre toujours dans une maison par la serrure ?", "clé"),
            ("Qu'il pleut, qu'il neige ou qu'il vente, je vais toujours à la mer, qui suis-je ?", "fleuve"),
            ("Quelle est la qualité que personne ne peut se vanter d'avoir ?", "modestie"),
            ("Je suis une table mais je n'ai pas de pieds, qui suis-je ?", "table de multiplication"),
            
            # Ajoute d'autres devinettes de niveau 2 ici...
        ]
        level_3_riddles = [
            ("Je me déplace sans pieds, je vole sans ailes, je te suis partout où tu vas. Qui suis-je?", "ombre"),
            ("Je suis invisible, mais on me sent. Je traverse les montagnes et les océans. Qui suis-je?", "vent"),
            ("Je suis toujours en mouvement mais je n’ai jamais de jambes. Qui suis-je?", "temps"),
            ("Je fais toujours du bruit, mais je ne parle pas. Qui suis-je ?", "la mer"),
            ("Je suis souvent blanc mais parfois coloré, et je peux vous faire pleurer. Qui suis-je ?", "oignon"),
            ("Je peux être cassé mais ne peux pas être réparé. Qui suis-je ?","silence"),
            ("Si deux frères et leur chien n'étaient pas sous un parapluie, pourquoi ne sont-ils pas trempés ?", "il ne pleuvait pas"),
            ("Imaginez que vous êtes dans une salle sans fenêtre et sans porte, comment sortez vous ?", "En arrêtant d’imaginer"),
            ("Un coq pond un oeuf sur la pointe d'un toit. De quel côté va rouler l'oeuf ?", "Les coqs ne pondent pas"),
            ("Un homme traverse une rivière sans être mouillé. Il n'a pas nagé ni utilisé de bateau ou de pont, comment a-t-il fait ?", "la rivière est gelée "),
            ("Quatre poissons sont dans un bocal, l'un d'entre eux meurt. Combien y-a-t-il de poissons dans le bocal ?", "quatre"),
            ("Je vous regarde, je vous ressemble si vous levez la main gauche, je lève la droite, qui suis-je ?", "mon reflet dans le miroir"),
            ("Un avion s'écrase entre la frontière française et belge, où enterre-t-on les survivants ?", "null part"),
            ("Que peut-on tenir dans sa main gauche mais pas dans sa droite ?", "son coup droit"),
            ("J'ai un chapeau mais pas de tête, j'ai un pied mais pas de chaussures, que suis-je ?", "champignon"),
            ("Plus il y en a, moins on voit, qu'est-ce que c'est ?", "obscurité"),
            
            # Ajoute d'autres devinettes de niveau 3 ici...
        ]

        available_riddles = []

        if self.level == 1:
            available_riddles = level_1_riddles
        elif self.level == 2:
            available_riddles = level_2_riddles
        elif self.level == 3:
            available_riddles = level_3_riddles

        # Filtrer les devinettes déjà utilisées
        unused_riddles = [r for r in available_riddles if r not in self.used_riddles]

        if not unused_riddles:  # Si toutes les devinettes ont été utilisées
            self.show_dialog("Félicitations", "Vous avez résolu toutes les devinettes de ce niveau !", "#00FF00")
            self.reset_game()
            return None  # Retourner None pour éviter d'utiliser une devinette

        return random.choice(unused_riddles)

    def check_guess(self, instance):
        user_guess = self.input_field.text.strip().lower()
        correct_answer = self.current_answer.lower()

        if user_guess == correct_answer:
            if hasattr(self, 'timer_event'):
                self.timer_event.cancel()  # Arrêter le timer si la réponse est correcte
            self.devinettes_resolues += 1
            self.score += 10  # Ajouter des points au score
            self.used_riddles.add((self.current_riddle, self.current_answer))  # Ajouter la devinette aux utilisées
            self.show_dialog("Bravo !", "Bonne réponse !", "#00FF00")
            
            # Utiliser un délai pour afficher la nouvelle devinette
            Clock.schedule_once(lambda dt: self.new_riddle(), 2)  # Changer à la nouvelle devinette après 2 secondes
        else:
            self.show_dialog("Oops !", "Mauvaise réponse.", "#FF0000")

    # Met à jour le score affiché
        self.score_label.text = f"Score: {self.score}"

    def new_riddle(self):
        """Charge une nouvelle devinette."""
        self.current_riddle, self.current_answer = self.get_random_riddle()
        if self.current_riddle:  # Vérifie si une nouvelle devinette a été obtenue
            self.riddle_label.text = f"Devinette : {self.current_riddle}"
            self.input_field.text = ""
            self.temps_restants = 1200 if self.level == 1 else 600 if self.level == 2 else 300
            self.start_timer()

    def reset_game(self):
        """Réinitialise le jeu avec une nouvelle devinette et redémarre le minuteur."""
        self.level = 1
        self.devinettes_resolues = 0
        self.used_riddles.clear()  # Réinitialiser les devinettes utilisées
        self.new_riddle()  # Charger une nouvelle devinette

    def check_niveau(self):
        """Passe au niveau suivant si toutes les devinettes du niveau sont résolues."""
        if self.devinettes_resolues >= self.devinettes_par_niveau:
            self.passer_au_niveau_suivant()

    def passer_au_niveau_suivant(self):
        """Passe au niveau suivant et ajuste le temps et la difficulté."""
        if self.level < 3:
            self.level += 1
            self.level_label.text = f"Niveau : {self.level}" 
            if self.level == 2:
                self.temps_restants = 600  # 10 minutes pour le niveau 2
                self.level_label.text = f"Niveau : {self.level}" 
            elif self.level == 3:
                self.temps_restants = 300  # 5 minutes pour le niveau 3
                self.level_label.text = f"Niveau : {self.level}" 
            self.devinettes_resolues = 0

        else:
            self.show_dialog("Félicitations", "Vous avez terminé tous les niveaux !", "#00FF00")

    def start_timer(self, dt=None):
        """Démarre ou redémarre le timer."""
        self.timer_label.text = f"Temps restant: {self.format_time(self.temps_restants)}"
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()  # Annuler l'ancien timer
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        """Met à jour le timer et gère le passage au niveau suivant."""
        self.temps_restants -= 1
        self.timer_label.text = f"Temps restant: {self.format_time(self.temps_restants)}"

        if self.temps_restants <= 0:
            self.timer_event.cancel()
            self.show_dialog("Temps écoulé !", "Vous avez perdu.", "#FF0000")
            self.reset_game()  # Réinitialiser le jeu après le temps écoulé

    def format_time(self, seconds):
        """Formate le temps restant en minutes et secondes."""
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"

    def show_dialog(self, title, message, color):
        content = BoxLayout(orientation='vertical')
        
        # Utiliser un bouton pour afficher le message
        message_button = Button(text=message, background_color=color)
        content.add_widget(message_button)

        ok_button = Button(text="OK")
        content.add_widget(ok_button)

        popup = Popup(title=title, content=content, size_hint=(0.6, 0.4))
        
        # Fermer le popup lorsque le bouton OK est cliqué
        ok_button.bind(on_release=popup.dismiss)

        popup.open()

    def pause_game(self, instance):
        """Met le jeu en pause."""
        if hasattr(self, 'timer_event'):
            self.timer_event.cancel()
        self.show_dialog("Pause", "Jeu mis en pause. Appuyez sur 'Reprendre' pour continuer.", "#FF8800")

if __name__ == "__main__":
    GuessRiddleApp().run()
