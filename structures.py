# --- PARTIE 1 : HISTORIQUE (PILE/LISTE CHAÎNÉE) ---

class Noeud:
    """Un maillon de la chaîne. Il contient la commande et le lien vers le suivant."""
    def __init__(self, data):
        self.data = data
        self.suivant = None

class HistoriquePile:
    """
    Gestion de l'historique sous forme de Pile (Stack).
    """
    def __init__(self):
        self.tete = None

    def empiler(self, commande):
        nouveau_noeud = Noeud(commande)
        nouveau_noeud.suivant = self.tete
        self.tete = nouveau_noeud

    def voir_dernier(self):
        if self.tete is None:
            return None
        return self.tete.data

    def recuperer_tout(self):
        commandes = []
        courant = self.tete
        while courant is not None:
            commandes.append(courant.data)
            courant = courant.suivant
        return commandes

    def vider(self):
        self.tete = None

    def charger_depuis_liste(self, liste_commandes):
        """Reconstruit la pile depuis une liste (pour le JSON)"""
        self.vider()
        for commande in reversed(liste_commandes):
            self.empiler(commande)


# --- PARTIE 2 : ARBRE DE DISCUSSION ---

class NoeudArbre:
    """
    Représente une étape de la conversation.
    """
    def __init__(self, texte):
        self.texte = texte
        self.enfants = {} 

    def ajouter_reponse(self, reponse, noeud_suivant):
        self.enfants[reponse.lower()] = noeud_suivant

    def est_feuille(self):
        return len(self.enfants) == 0


class ArbreDiscussion:
    def __init__(self):
        self.racine = None
        
    def creer_scenario_par_defaut(self):
        """
        Scénario : Marvel Rivals COMPLET (Tanks + Supports + DPS)
        """
        # --- 1. LES DONNÉES ---
        liste_tanks = ["Captain America", "Doctor Strange", "Groot", "Hulk", "Magneto", "Thor", "Peni Parker", "Venom"]
        liste_supports = ["Adam Warlock", "Cloak & Dagger", "Jeff the Land Shark", "Loki", "Luna Snow", "Mantis", "Rocket Raccoon"]
        liste_dps = ["Black Panther", "Black Widow", "Hawkeye", "Hela", "Iron Fist", "Iron Man", "Magik", "Namor", "The Punisher", "Scarlet Witch", "Spider Man", "Star Lord", "Storm", "Moon Knight", "Psylocke", "Squirrel Girl", "Winter Soldier", "Wolverine"]

        # --- 2. CRÉATION DES QUESTIONS ---

        racine = NoeudArbre("Joues-tu à Marvel Rivals ? (oui/non)")
        fin_non = NoeudArbre("Dommage, c'est un super jeu ! Bye.")
        q_role = NoeudArbre("Quel rôle joues-tu ? (Tank/Support/DPS)")

        # Menus de choix
        texte_tanks = "Quel Tank ?\n- " + "\n- ".join(liste_tanks)
        q_choix_tank = NoeudArbre(texte_tanks)

        texte_supports = "Quel Support ?\n- " + "\n- ".join(liste_supports)
        q_choix_support = NoeudArbre(texte_supports)

        texte_dps = "Quel DPS ?\n- " + "\n- ".join(liste_dps)
        q_choix_dps = NoeudArbre(texte_dps)

        # --- 3. LES RÉPONSES SPÉCIFIQUES ---

        # === TANKS ===
        fin_cap = NoeudArbre("Pas mal, tiens des tips pratiques si tu veux être un très bon Captain ! : https://www.youtube.com/watch?v=G2JVqDJ3IdM")
        fin_strange = NoeudArbre("Okay ! Tiens si tu veux être le meilleur manieur de l'oeil d'agamotto : https://youtu.be/XvO5F2Be2ak")
        fin_groot = NoeudArbre("Je s'appelle GROOT !!!! (des petits tips cool à savoir dessus) : https://www.youtube.com/watch?v=Ww9q9WEg7j8")
        fin_hulk = NoeudArbre("Ah ouais tu es un bourrin toi ! Tiens pour survivre plus longtemps : https://www.youtube.com/watch?v=TfXUVl-eD7M")
        fin_magneto = NoeudArbre("FEAR MAGNETO !!! Continue à solo ult CD et Jeff et pour être meilleur : https://www.youtube.com/watch?v=rRHWCMrfOqM")
        fin_thor = NoeudArbre("Bon Tank mais n'oublie pas de protéger ta backline quand ils en ont besoin ! Petit conseil dessus : https://www.youtube.com/watch?v=T4wTnvQ5YoY")
        fin_peni = NoeudArbre("Bon choix mais arrête de forcer le pick en la jouant en attaque ! Pour être plus efficace dessus : https://www.youtube.com/watch?v=J0P3z9_4sMU")
        fin_venom = NoeudArbre("Continue à dive la backline c'est la meilleure façon d'être impactant avec ! Les combos utiles à savoir sur le héro : https://www.youtube.com/watch?v=IxoahJ0FlUM")

        # === SUPPORTS ===
        fin_adam = NoeudArbre("Pas évident mais bon choix ! Tiens des conseils pour être meilleur dessus : https://www.youtube.com/watch?v=MSF-wmXJJHg")
        fin_cloak = NoeudArbre("Pas fan perso mais ultime broken ! Pour mieux survivre avec : https://www.youtube.com/watch?v=YhRC1TgCOLk")
        fin_jeff = NoeudArbre("MRRRR ! https://www.youtube.com/watch?v=XBVUvqn9ogE")
        fin_loki = NoeudArbre("ctrl+c  ctrl+v  press q , team kill ez : https://www.youtube.com/watch?v=7wODhk-0EDc")
        fin_luna = NoeudArbre("On se demande quel skin tu joues dessus hein ! Pour mieux heal avec : https://www.youtube.com/watch?v=sYxHj4hJ1l0")
        fin_mantis = NoeudArbre("Bon support pour du 3 heal mais ne fonctionne pas tout le temps ! Pour bien la jouer : https://www.youtube.com/watch?v=57nZpUUHbZI")
        fin_rocket = NoeudArbre("Heal simple, peut rez, bon choix ! Pour utiliser tout son potentiel : https://www.youtube.com/watch?v=pJcCiHHgwV0")

        # === DPS ===
        fin_bpanther = NoeudArbre("Si tu es une merde dessus arrête de le jouer ! Mais au cas ou ça peut t'aider : https://www.youtube.com/watch?v=L9ENiiPO1Mk")
        fin_bwidow = NoeudArbre("Change de jeu... ! Tu seras peut être utile avec ça : https://www.youtube.com/watch?v=LMej9-pVFek")
        fin_hawkeye = NoeudArbre("Tire sans viser tu toucheras forcement, sinon press q spam et voilà 3 kills minimums ! Au cas ou : https://www.youtube.com/watch?v=L10v3F9r5Hs")
        fin_hela = NoeudArbre("Voilà ça c'est bien, mais il faut réussir à toucher ! Pour être meilleur : https://www.youtube.com/watch?v=KD6ORSun0ZE")
        fin_ironfist = NoeudArbre("LÀ-HAUT, DANS LE CIEL… Est-ce un oiseau ? Est-ce un avion ? Non, c'est... Iron Fist... ! Pour être efficace : https://www.youtube.com/watch?v=rIlhe94-oBA")
        fin_ironman = NoeudArbre("Jarvis clip that : https://www.youtube.com/watch?v=3hV4kz3Repc")
        fin_magik = NoeudArbre("Soit tu es bon soit tu es mauvais avec ! Pour être parmi les bons : https://www.youtube.com/watch?v=QpXA63YtVwo")
        fin_namor = NoeudArbre("Toi tu aimes les pieds ! Tiens pour voir plus les kills que ses pieds : https://www.youtube.com/watch?v=4wg6f_4Hvb4")
        fin_punisher = NoeudArbre("Tu es la définition du rôle DPS ! Pour mieux taper : https://www.youtube.com/watch?v=T0d2S3gRW-M")
        fin_scarlet = NoeudArbre("Tu dois surement jouer les yeux fermés ! https://www.youtube.com/watch?v=s0GwCyoyeas")
        fin_spiderman = NoeudArbre("Arrête de jouer ça pue !")
        fin_starlord = NoeudArbre("Tracer de wish ! Ca peut servir : https://www.youtube.com/watch?v=71rolJfkehc")
        fin_storm = NoeudArbre("Bon perso ! Quelques tips : https://www.youtube.com/watch?v=lfVw8koF5YQ")
        fin_moonknight = NoeudArbre("T'es qu'une merde qui sait pas jouer !")
        fin_psylocke = NoeudArbre("Intéressant ! Des conseils pour t'améliorer : https://www.youtube.com/watch?v=zFqoRL315N4")
        fin_squirrel = NoeudArbre("pfffff.... ça peut être efficace mais on baille fort")
        fin_winter = NoeudArbre("ARMED AND DANGEROUS.... AGAIN... AGAIN... AGAIN... AGAIN... ! Pour encore plus spam son ult : https://www.youtube.com/watch?v=zv8X2yYRKQc")
        fin_wolverine = NoeudArbre("Grab encore et toujours plus ! Pour grab plus facilement : https://www.youtube.com/watch?v=YWExxrcIMSo")

        # --- 4. CRÉATION DES LIENS (MAPPING) ---

        # Navigation principale
        racine.ajouter_reponse("non", fin_non)
        racine.ajouter_reponse("oui", q_role)
        q_role.ajouter_reponse("tank", q_choix_tank)
        q_role.ajouter_reponse("support", q_choix_support)
        q_role.ajouter_reponse("dps", q_choix_dps)

        # Liens TANK
        q_choix_tank.ajouter_reponse("Captain America", fin_cap)
        q_choix_tank.ajouter_reponse("Doctor Strange", fin_strange)
        q_choix_tank.ajouter_reponse("Groot", fin_groot)
        q_choix_tank.ajouter_reponse("Hulk", fin_hulk)
        q_choix_tank.ajouter_reponse("Magneto", fin_magneto)
        q_choix_tank.ajouter_reponse("Thor", fin_thor)
        q_choix_tank.ajouter_reponse("Peni Parker", fin_peni)
        q_choix_tank.ajouter_reponse("Venom", fin_venom)

        # Liens SUPPORTS
        q_choix_support.ajouter_reponse("Adam Warlock", fin_adam)
        q_choix_support.ajouter_reponse("Cloak & Dagger", fin_cloak)
        q_choix_support.ajouter_reponse("Jeff the Land Shark", fin_jeff)
        q_choix_support.ajouter_reponse("Loki", fin_loki)
        q_choix_support.ajouter_reponse("Luna Snow", fin_luna)
        q_choix_support.ajouter_reponse("Mantis", fin_mantis)
        q_choix_support.ajouter_reponse("Rocket Raccoon", fin_rocket)

        # Liens DPS
        q_choix_dps.ajouter_reponse("Black Panther", fin_bpanther)
        q_choix_dps.ajouter_reponse("Black Widow", fin_bwidow)
        q_choix_dps.ajouter_reponse("Hawkeye", fin_hawkeye)
        q_choix_dps.ajouter_reponse("Hela", fin_hela)
        q_choix_dps.ajouter_reponse("Iron Fist", fin_ironfist)
        q_choix_dps.ajouter_reponse("Iron Man", fin_ironman)
        q_choix_dps.ajouter_reponse("Magik", fin_magik)
        q_choix_dps.ajouter_reponse("Namor", fin_namor)
        q_choix_dps.ajouter_reponse("The Punisher", fin_punisher)
        q_choix_dps.ajouter_reponse("Scarlet Witch", fin_scarlet)
        q_choix_dps.ajouter_reponse("Spider Man", fin_spiderman)
        q_choix_dps.ajouter_reponse("Star Lord", fin_starlord)
        q_choix_dps.ajouter_reponse("Storm", fin_storm)
        q_choix_dps.ajouter_reponse("Moon Knight", fin_moonknight)
        q_choix_dps.ajouter_reponse("Psylocke", fin_psylocke)
        q_choix_dps.ajouter_reponse("Squirrel Girl", fin_squirrel)
        q_choix_dps.ajouter_reponse("Winter Soldier", fin_winter)
        q_choix_dps.ajouter_reponse("Wolverine", fin_wolverine)

        # --- 5. DÉMARRAGE ---
        self.racine = racine

    def rechercher_sujet(self, mot_cle):
        """Fonctionnalité 'speak about X'"""
        return self._recherche_recursive(self.racine, mot_cle.lower())

    def _recherche_recursive(self, noeud, mot):
        if noeud is None:
            return False
        if mot in noeud.texte.lower():
            return True
        for reponse, enfant in noeud.enfants.items():
            if mot in reponse:
                return True
            if self._recherche_recursive(enfant, mot):
                return True
        return False