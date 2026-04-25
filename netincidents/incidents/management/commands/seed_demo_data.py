from datetime import timedelta

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from incidents.models import (
    Commentaire,
    Equipement,
    HistoriqueStatut,
    Incident,
    Notification,
    ProfilUtilisateur,
)


DEMO_USERS = [
    {
        "username": "admin",
        "email": "admin@netincidents.local",
        "password": "admin123",
        "first_name": "Awa",
        "last_name": "Kone",
        "role": "admin",
        "departement": "DSI",
        "telephone": "+225 07 00 00 00",
        "is_superuser": True,
        "is_staff": True,
    },
    {
        "username": "technicien1",
        "email": "tech1@netincidents.local",
        "password": "tech123",
        "first_name": "Kouassi",
        "last_name": "Aman",
        "role": "technicien",
        "departement": "Reseau",
        "telephone": "+225 07 11 22 33",
    },
    {
        "username": "technicien2",
        "email": "tech2@netincidents.local",
        "password": "tech456",
        "first_name": "Mariam",
        "last_name": "Traore",
        "role": "technicien",
        "departement": "Exploitation",
        "telephone": "+225 05 22 33 44",
    },
    {
        "username": "superviseur",
        "email": "sup@netincidents.local",
        "password": "sup123",
        "first_name": "Adjoua",
        "last_name": "Brou",
        "role": "superviseur",
        "departement": "Pilotage",
        "telephone": "+225 01 98 76 54",
    },
    {
        "username": "utilisateur1",
        "email": "user1@netincidents.local",
        "password": "user123",
        "first_name": "Nadia",
        "last_name": "Yao",
        "role": "utilisateur",
        "departement": "Finance",
        "telephone": "+225 07 77 88 99",
    },
]

EQUIPEMENTS = [
    {
        "nom": "Switch Coeur Bat. A",
        "type_equipement": "switch",
        "adresse_ip": "10.0.0.1",
        "localisation": "Batiment A - Salle serveurs",
        "description": "Switch de coeur desservant les etages du batiment A.",
        "statut": "actif",
    },
    {
        "nom": "Routeur Principal MPLS",
        "type_equipement": "routeur",
        "adresse_ip": "192.168.1.1",
        "localisation": "Datacenter central",
        "description": "Routeur d'interconnexion WAN et MPLS.",
        "statut": "actif",
    },
    {
        "nom": "Firewall Perimetrique",
        "type_equipement": "firewall",
        "adresse_ip": "10.10.0.1",
        "localisation": "DMZ - Entree reseau",
        "description": "Filtrage principal des flux entrants et sortants.",
        "statut": "actif",
    },
    {
        "nom": "Serveur DNS Primaire",
        "type_equipement": "serveur",
        "adresse_ip": "10.0.0.53",
        "localisation": "Datacenter central",
        "description": "Resolution DNS pour les applications internes.",
        "statut": "actif",
    },
    {
        "nom": "Switch Acces Bureau 2",
        "type_equipement": "switch",
        "adresse_ip": "10.1.2.10",
        "localisation": "Batiment B - 2e etage",
        "description": "Distribution locale pour les postes bureautiques.",
        "statut": "actif",
    },
    {
        "nom": "AP Wi-Fi Cafeteria",
        "type_equipement": "point_acces",
        "adresse_ip": "10.2.0.15",
        "localisation": "Cafeteria RDC",
        "description": "Point d'acces public interne a forte densite.",
        "statut": "maintenance",
    },
    {
        "nom": "Lien Fibre Operateur A",
        "type_equipement": "lien_wan",
        "adresse_ip": None,
        "localisation": "POP operateur - Plateau",
        "description": "Lien principal Internet / cloud.",
        "statut": "actif",
    },
    {
        "nom": "Switch Distribution RDC",
        "type_equipement": "switch",
        "adresse_ip": "10.0.1.2",
        "localisation": "Batiment C - RDC",
        "description": "Switch de distribution pour les plateaux RDC.",
        "statut": "inactif",
    },
    {
        "nom": "Serveur Supervision NMS",
        "type_equipement": "serveur",
        "adresse_ip": "10.0.5.20",
        "localisation": "Salle NOC",
        "description": "Collecte SNMP, alertes et supervision de capacite.",
        "statut": "actif",
    },
]

INCIDENTS = [
    {
        "slug": "switch-coeur",
        "titre": "Panne totale du switch coeur Batiment A",
        "description": "Le switch principal ne repond plus depuis 14h30 et l'ensemble du batiment A est isole du reseau.",
        "categorie": "panne_reseau",
        "priorite": "critique",
        "statut": "en_cours",
        "impact": "Environ 150 utilisateurs sans acces au SI et a la telephonie IP.",
        "cause_racine": "Surchauffe du module d'alimentation apres une coupure de climatisation.",
        "solution_appliquee": "",
        "cree_par": "utilisateur1",
        "assigne_a": "technicien1",
        "equipements": ["Switch Coeur Bat. A"],
        "days_ago": 1,
        "history": [
            ("", "ouvert", "utilisateur1", "Signalement initial"),
            ("ouvert", "en_cours", "admin", "Affecte a technicien1 pour intervention sur site"),
        ],
        "commentaires": [
            ("technicien1", "action", "Intervention sur site en cours. Le chassis reste inaccessible en console."),
            ("admin", "escalade", "Commande express du module d'alimentation lancee chez le fournisseur."),
        ],
    },
    {
        "slug": "wifi-cafeteria",
        "titre": "Lenteurs sur le Wi-Fi de la cafeteria",
        "description": "Les utilisateurs constatent des debits inferieurs a 1 Mbps pendant les heures de forte affluence.",
        "categorie": "lenteur",
        "priorite": "haute",
        "statut": "ouvert",
        "impact": "Les applications cloud sont difficilement utilisables a la pause de midi.",
        "cause_racine": "",
        "solution_appliquee": "",
        "cree_par": "utilisateur1",
        "assigne_a": "admin",
        "equipements": ["AP Wi-Fi Cafeteria"],
        "days_ago": 2,
        "history": [
            ("", "ouvert", "utilisateur1", "Creation du ticket"),
        ],
        "commentaires": [
            ("superviseur", "commentaire", "Verifier la saturation radio et la densite des clients associes."),
        ],
    },
    {
        "slug": "tentatives-intrusion",
        "titre": "Tentatives d'intrusion detectees sur le firewall",
        "description": "Le SIEM remonte un pic de tentatives SSH provenant de plusieurs adresses IP externes.",
        "categorie": "securite",
        "priorite": "critique",
        "statut": "en_cours",
        "impact": "Risque de compromission du perimetre et mobilisation de l'equipe securite.",
        "cause_racine": "Regle temporaire trop permissive sur le port 22.",
        "solution_appliquee": "Blocage des IP sources et restriction ACL initiale.",
        "cree_par": "admin",
        "assigne_a": "technicien2",
        "equipements": ["Firewall Perimetrique"],
        "days_ago": 1,
        "history": [
            ("", "ouvert", "admin", "Alerte remontee par le SIEM"),
            ("ouvert", "en_cours", "admin", "Affecte a technicien2 pour containment"),
        ],
        "commentaires": [
            ("technicien2", "action", "Les flux suspects sont bloques. Extraction des journaux pour analyse."),
        ],
    },
    {
        "slug": "wan-operateur",
        "titre": "Perte de connectivite du lien WAN operateur",
        "description": "Le lien fibre principal est tombe a 08h15. Le backup 4G a pris le relais avec une bande passante reduite.",
        "categorie": "connectivite",
        "priorite": "haute",
        "statut": "resolu",
        "impact": "Degradation notable de l'acces Internet et des applications SaaS.",
        "cause_racine": "Rupture physique de fibre lors de travaux exterieurs.",
        "solution_appliquee": "Intervention de l'operateur et retour sur le lien principal apres validation.",
        "cree_par": "admin",
        "assigne_a": "technicien1",
        "equipements": ["Routeur Principal MPLS", "Lien Fibre Operateur A"],
        "days_ago": 5,
        "resolved_after_hours": 11,
        "history": [
            ("", "ouvert", "admin", "Detection automatique par la supervision"),
            ("ouvert", "en_cours", "admin", "Intervention operateur engagee"),
            ("en_cours", "resolu", "technicien1", "Lien retabli et tests conformes"),
        ],
        "commentaires": [
            ("technicien1", "mise_a_jour", "Le lien secondaire absorbe le trafic critique en attendant le retour operateur."),
            ("technicien1", "action", "Tests de debit et de latence valides apres retablissement."),
        ],
    },
    {
        "slug": "vlan-bureau-2",
        "titre": "Erreur de configuration VLAN sur le bureau 2",
        "description": "Les postes du bureau 2 ne peuvent plus joindre l'imprimante et certains services internes apres une maintenance.",
        "categorie": "configuration",
        "priorite": "moyenne",
        "statut": "resolu",
        "impact": "12 utilisateurs bloques sur l'impression reseau et certains lecteurs partages.",
        "cause_racine": "Mauvais tag VLAN sur le trunk principal.",
        "solution_appliquee": "Correction de la configuration puis validation avec les utilisateurs.",
        "cree_par": "superviseur",
        "assigne_a": "technicien1",
        "equipements": ["Switch Acces Bureau 2"],
        "days_ago": 10,
        "resolved_after_hours": 4,
        "history": [
            ("", "ouvert", "superviseur", "Ticket remonte par les utilisateurs du service"),
            ("ouvert", "en_cours", "admin", "Diagnostic switch en cours"),
            ("en_cours", "resolu", "technicien1", "Correction du trunk et validation"),
        ],
    },
    {
        "slug": "dns-intermittent",
        "titre": "Serveur DNS primaire intermittent",
        "description": "Des echecs DNS sporadiques apparaissent depuis trois jours sur plusieurs applications internes.",
        "categorie": "logiciel",
        "priorite": "haute",
        "statut": "ouvert",
        "impact": "Navigation lente et timeouts applicatifs aleatoires.",
        "cause_racine": "",
        "solution_appliquee": "",
        "cree_par": "utilisateur1",
        "assigne_a": "admin",
        "equipements": ["Serveur DNS Primaire", "Serveur Supervision NMS"],
        "days_ago": 3,
        "history": [
            ("", "ouvert", "utilisateur1", "Signalement par le support de proximite"),
        ],
        "commentaires": [
            ("admin", "commentaire", "Comparer la charge CPU et les timeouts entre DNS primaire et secondaire."),
        ],
    },
    {
        "slug": "switch-rdc",
        "titre": "Switch RDC Batiment C hors tension",
        "description": "Un switch a ete coupe pendant une maintenance electrique planifiee puis oublie hors tension.",
        "categorie": "materiel",
        "priorite": "moyenne",
        "statut": "ferme",
        "impact": "Plateau RDC sans reseau pendant 45 minutes.",
        "cause_racine": "Erreur de reperage du circuit electrique.",
        "solution_appliquee": "Remise sous tension et mise a jour de la procedure de maintenance.",
        "cree_par": "superviseur",
        "assigne_a": "technicien2",
        "equipements": ["Switch Distribution RDC"],
        "days_ago": 15,
        "resolved_after_hours": 1,
        "closed_after_hours": 6,
        "history": [
            ("", "ouvert", "superviseur", "Incident declare par le batiment C"),
            ("ouvert", "en_cours", "admin", "Technicien envoye sur site"),
            ("en_cours", "resolu", "technicien2", "Service restaure"),
            ("resolu", "ferme", "admin", "Retour d'experience valide"),
        ],
    },
    {
        "slug": "mpls-saturation",
        "titre": "Saturation de bande passante du lien MPLS",
        "description": "Le lien principal est monte a 98% d'utilisation et la VoIP devient instable.",
        "categorie": "lenteur",
        "priorite": "haute",
        "statut": "en_cours",
        "impact": "Qualite vocale degradee et visios instables sur plusieurs sites.",
        "cause_racine": "Sauvegarde non planifiee vers un site distant pendant les heures de bureau.",
        "solution_appliquee": "Arret du flux parasite et ajustement de la QoS en attendant la normalisation.",
        "cree_par": "superviseur",
        "assigne_a": "technicien2",
        "equipements": ["Routeur Principal MPLS", "Serveur Supervision NMS"],
        "days_ago": 0,
        "history": [
            ("", "ouvert", "superviseur", "Alerte capacite recue dans le NOC"),
            ("ouvert", "en_cours", "admin", "Priorisation du trafic VoIP"),
        ],
        "commentaires": [
            ("technicien2", "action", "Les flux de sauvegarde ont ete identifies et stoppes."),
        ],
    },
]

NOTIFICATIONS = [
    ("technicien1", "switch-coeur", "Nouvel incident critique assigne : panne switch coeur."),
    ("technicien2", "tentatives-intrusion", "Analyse securite prioritaire en cours sur le firewall."),
    ("utilisateur1", "wan-operateur", "Votre incident WAN a ete resolu."),
    ("admin", "dns-intermittent", "Incident DNS en attente d'affectation technique."),
]


class Command(BaseCommand):
    help = "Charge des donnees de demonstration coherentes pour le dashboard et les tests de connexion."

    def handle(self, *args, **options):
        with transaction.atomic():
            users = self._seed_users()
            equipments = self._seed_equipements()
            incidents = self._seed_incidents(users, equipments)
            self._seed_notifications(users, incidents)

        self.stdout.write(self.style.SUCCESS("Donnees de demonstration chargees avec succes."))
        self.stdout.write("")
        self.stdout.write("Comptes de test :")
        for user in DEMO_USERS:
            self.stdout.write(
                f"  - {user['username']} / {user['password']} ({user['role']})"
            )

    def _seed_users(self):
        users = {}
        for config in DEMO_USERS:
            user, created = User.objects.get_or_create(
                username=config["username"],
                defaults={
                    "email": config["email"],
                    "first_name": config["first_name"],
                    "last_name": config["last_name"],
                    "is_staff": config.get("is_staff", False),
                    "is_superuser": config.get("is_superuser", False),
                },
            )
            changed = created
            for field in ["email", "first_name", "last_name"]:
                value = config[field]
                if getattr(user, field) != value:
                    setattr(user, field, value)
                    changed = True

            for field in ["is_staff", "is_superuser"]:
                value = config.get(field, False)
                if getattr(user, field) != value:
                    setattr(user, field, value)
                    changed = True

            if not user.check_password(config["password"]):
                user.set_password(config["password"])
                changed = True

            if changed:
                user.save()

            profil, _ = ProfilUtilisateur.objects.get_or_create(user=user)
            profil.role = config["role"]
            profil.departement = config["departement"]
            profil.telephone = config["telephone"]
            profil.derniere_activite = timezone.now() - timedelta(minutes=2)
            profil.save()
            users[config["username"]] = user
        return users

    def _seed_equipements(self):
        equipments = {}
        for config in EQUIPEMENTS:
            equipement, _ = Equipement.objects.update_or_create(
                nom=config["nom"],
                defaults={
                    "type_equipement": config["type_equipement"],
                    "adresse_ip": config["adresse_ip"],
                    "localisation": config["localisation"],
                    "description": config["description"],
                    "statut": config["statut"],
                },
            )
            equipments[config["nom"]] = equipement
        return equipments

    def _seed_incidents(self, users, equipments):
        incidents = {}
        for config in INCIDENTS:
            incident, _ = Incident.objects.update_or_create(
                titre=config["titre"],
                defaults={
                    "description": config["description"],
                    "categorie": config["categorie"],
                    "priorite": config["priorite"],
                    "statut": config["statut"],
                    "impact": config["impact"],
                    "cause_racine": config["cause_racine"],
                    "solution_appliquee": config["solution_appliquee"],
                    "cree_par": users[config["cree_par"]],
                    "assigne_a": users[config["assigne_a"]] if config.get("assigne_a") else None,
                },
            )

            created_at = timezone.now() - timedelta(days=config["days_ago"])
            Incident.objects.filter(pk=incident.pk).update(date_creation=created_at)
            incident.refresh_from_db()

            resolution_date = None
            fermeture_date = None
            if config["statut"] in {"resolu", "ferme"}:
                resolution_date = created_at + timedelta(hours=config.get("resolved_after_hours", 2))
            if config["statut"] == "ferme":
                fermeture_date = resolution_date + timedelta(hours=config.get("closed_after_hours", 2))

            incident.date_resolution = resolution_date
            incident.date_fermeture = fermeture_date
            incident.save(update_fields=["date_resolution", "date_fermeture", "date_modification"])

            incident.equipements.set([equipments[name] for name in config["equipements"]])

            Commentaire.objects.filter(incident=incident).delete()
            HistoriqueStatut.objects.filter(incident=incident).delete()

            base_date = created_at
            for index, (ancien, nouveau, auteur, commentaire) in enumerate(config.get("history", [])):
                history = HistoriqueStatut.objects.create(
                    incident=incident,
                    ancien_statut=ancien,
                    nouveau_statut=nouveau,
                    modifie_par=users[auteur],
                    commentaire=commentaire,
                )
                HistoriqueStatut.objects.filter(pk=history.pk).update(
                    date_changement=base_date + timedelta(hours=index)
                )

            for index, (auteur, type_commentaire, contenu) in enumerate(config.get("commentaires", [])):
                commentaire = Commentaire.objects.create(
                    incident=incident,
                    auteur=users[auteur],
                    type_commentaire=type_commentaire,
                    contenu=contenu,
                )
                Commentaire.objects.filter(pk=commentaire.pk).update(
                    date_creation=base_date + timedelta(hours=index, minutes=20)
                )

            incidents[config["slug"]] = incident
        return incidents

    def _seed_notifications(self, users, incidents):
        Notification.objects.filter(
            utilisateur__username__in=[config["username"] for config in DEMO_USERS]
        ).delete()

        now = timezone.now()
        for index, (username, incident_slug, message) in enumerate(NOTIFICATIONS):
            notification = Notification.objects.create(
                utilisateur=users[username],
                incident=incidents[incident_slug],
                message=message,
                lue=False,
            )
            Notification.objects.filter(pk=notification.pk).update(
                date_creation=now - timedelta(minutes=index * 7)
            )
