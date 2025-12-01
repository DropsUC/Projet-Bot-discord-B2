import discord
import os
import json
import random
import asyncio
from dotenv import load_dotenv
from discord.ext import commands
import structures

load_dotenv()

print("Lancement du bot...")
bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

# --- CONFIGURATION ---
FICHIER_SAUVEGARDE = "data.json"
historiques = {}
etats_discussion = {}

# Initialisation de l'arbre
arbre_discussion = structures.ArbreDiscussion()
arbre_discussion.creer_scenario_par_defaut()

# --- FONCTIONS DE GESTION DES DONNÉES ---

def sauvegarder_donnees():
    """Sauvegarde les historiques dans le fichier JSON."""
    data = {}
    for user_id, pile in historiques.items():
        data[str(user_id)] = pile.recuperer_tout()
        
    with open(FICHIER_SAUVEGARDE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def charger_donnees():
    """Charge les historiques depuis le fichier JSON au démarrage."""
    if not os.path.exists(FICHIER_SAUVEGARDE):
        return

    try:
        with open(FICHIER_SAUVEGARDE, "r", encoding="utf-8") as f:
            data = json.load(f)
            
        for user_id_str, liste_commandes in data.items():
            user_id = int(user_id_str)
            pile = structures.HistoriquePile()
            pile.charger_depuis_liste(liste_commandes)
            historiques[user_id] = pile
        print("Données chargées depuis data.json !")
    except Exception as e:
        print(f"Erreur de chargement : {e}")

# --- ÉVÉNEMENTS ---

@bot.event
async def on_ready():
    print("Bot allumé !")
    charger_donnees()
    try:
        synced = await bot.tree.sync()
        print(f"Commandes slash synchronisées : {len(synced)}")
    except Exception as e:
        print(e)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    
    user_id = message.author.id

    # 1. Gestion de l'historique
    if user_id not in historiques:
        historiques[user_id] = structures.HistoriquePile()
    
    historiques[user_id].empiler(message.content)
    sauvegarder_donnees() 
    
    # 2. Gestion de l'arbre de discussion
    if user_id in etats_discussion:
        noeud_actuel = etats_discussion[user_id]
        reponse_user = message.content.lower().strip() 

        if reponse_user in noeud_actuel.enfants:
            prochain_noeud = noeud_actuel.enfants[reponse_user]
            etats_discussion[user_id] = prochain_noeud
            
            await message.channel.send(prochain_noeud.texte)

            if prochain_noeud.est_feuille():
                del etats_discussion[user_id]
                await message.channel.send("--- Fin de la discussion ---")
        else:
            choix = list(noeud_actuel.enfants.keys())
            await message.channel.send(f"Je ne comprends pas. Réponses possibles : {', '.join(choix)}")
        return 

    await bot.process_commands(message)

# --- COMMANDES : HISTORIQUE ---

@bot.tree.command(name="last_cmd", description="Voir ma dernière commande")
async def last_cmd(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in historiques and historiques[user_id].voir_dernier():
        dernier = historiques[user_id].voir_dernier()
        await interaction.response.send_message(f"Dernière commande : `{dernier}`")
    else:
        await interaction.response.send_message("Aucun historique.")

@bot.tree.command(name="all_history", description="Voir tout mon historique")
async def all_history(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in historiques:
        liste = historiques[user_id].recuperer_tout()
        if not liste:
             await interaction.response.send_message("Historique vide.")
             return
        
        reponse = "**Ton historique :**\n```\n" + "\n".join(liste[:20]) + "\n```"
        await interaction.response.send_message(reponse)
    else:
        await interaction.response.send_message("Aucun historique trouvé.")

@bot.tree.command(name="clear_history", description="Vider mon historique")
async def clear_history(interaction: discord.Interaction):
    user_id = interaction.user.id
    if user_id in historiques:
        historiques[user_id].vider()
        sauvegarder_donnees()
        await interaction.response.send_message("Historique vidé.")
    else:
        await interaction.response.send_message("Rien à vider.")

# --- COMMANDES : DISCUSSION ---

@bot.tree.command(name="discussion", description="Lancer le questionnaire")
async def discussion(interaction: discord.Interaction):
    user_id = interaction.user.id
    etats_discussion[user_id] = arbre_discussion.racine
    await interaction.response.send_message(f"C'est parti !\n{arbre_discussion.racine.texte}")

@bot.tree.command(name="reset", description="Recommence la discussion")
async def reset(interaction: discord.Interaction):
    user_id = interaction.user.id
    etats_discussion[user_id] = arbre_discussion.racine
    await interaction.response.send_message(f"Discussion réinitialisée.\n{arbre_discussion.racine.texte}")

@bot.tree.command(name="speak_about", description="Vérifie si un sujet existe")
async def speak_about(interaction: discord.Interaction, sujet: str):
    trouve = arbre_discussion.rechercher_sujet(sujet)
    if trouve:
        await interaction.response.send_message(f"OUI ! Le sujet '{sujet}' est traité.")
    else:
        await interaction.response.send_message(f"NON. Je ne parle pas de '{sujet}'.")

# --- COMMANDES : BONUS & UTILITAIRES ---

@bot.tree.command(name="dès", description="Lance un dé (1-6)")
async def dice(interaction: discord.Interaction):
    await interaction.response.send_message(f"🎲 Résultat : **{random.randint(1, 6)}**")

@bot.tree.command(name="supp", description="Supprime les X derniers messages")
async def supp(interaction: discord.Interaction, nombre: int):
    await interaction.response.defer(ephemeral=True)

    if 1 <= nombre <= 20:
        await interaction.channel.purge(limit=nombre)
        await interaction.followup.send(f"✅ J'ai supprimé les {nombre} derniers messages.", ephemeral=True)
    else:
        await interaction.followup.send("❌ Choisis un nombre entre 1 et 20 s'il te plaît.", ephemeral=True)

@bot.tree.command(name="commands", description="Affiche la liste de toutes les commandes disponibles")
async def show_commands(interaction: discord.Interaction):
    embed = discord.Embed(
        title="📜 Liste des commandes",
        description="Voici toutes les fonctionnalités disponibles :",
        color=discord.Color.gold()
    )

    for commande in bot.tree.get_commands():
        embed.add_field(name=f"/{commande.name}", value=commande.description, inline=False)

    await interaction.response.send_message(embed=embed)    

bot.run(os.getenv('DISCORD_TOKEN'))