import argparse
from fingerprint_system import FingerprintDatabase


def main() -> None:
    parser = argparse.ArgumentParser(description="Système d'authentification biométrique par empreinte digitale")
    subparsers = parser.add_subparsers(dest="command", required=True)

    register_parser = subparsers.add_parser("register", help="Enregistrer un utilisateur")
    register_parser.add_argument("--user-id", required=True, help="Identifiant de l'utilisateur")
    register_parser.add_argument("--sample", required=True, help="Valeur de l'empreinte à enregistrer")

    verify_parser = subparsers.add_parser("verify", help="Vérifier une empreinte")
    verify_parser.add_argument("--user-id", required=True, help="Identifiant de l'utilisateur")
    verify_parser.add_argument("--sample", required=True, help="Valeur de l'empreinte à comparer")
    verify_parser.add_argument("--threshold", type=float, default=0.90, help="Seuil de similarité (0 à 1)")

    list_parser = subparsers.add_parser("list", help="Lister les utilisateurs enregistrés")

    args = parser.parse_args()
    database = FingerprintDatabase("data/fingerprints.json")

    if args.command == "register":
        database.register_user(args.user_id, args.sample)
        print(f"Utilisateur {args.user_id} enregistré avec succès.")
        return

    if args.command == "verify":
        ok, score = database.verify(args.user_id, args.sample, threshold=args.threshold)
        if ok:
            print("Authentification acceptée.")
        else:
            print("Authentification refusée.")
        print(f"Score de similarité : {score:.4f}")
        return

    if args.command == "list":
        users = database.list_users()
        if not users:
            print("Aucun utilisateur enregistré.")
            return
        print("Utilisateurs enregistrés :")
        for user in users:
            print(f"- {user}")
        return


if __name__ == "__main__":
    main()
