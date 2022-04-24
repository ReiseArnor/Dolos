import logging
import sys
import getopt

from dolos.util import clear_screen, logger
from dolos.watch import watch_anime


def main(argv):
    anime = None
    episode = None
    anime_site = "monoschinos"
    SITES_LIST = ["monoschinos", "animeflv"]

    try:
        opts, _ = getopt.getopt(
            argv, "ha:e:p:", ["anime=", "episodio=", "pagina=", "debug"])
    except getopt.GetoptError:
        print('dolos -a <anime> -e <episodio>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(
                """dolos -a <anime> -e <episodio>
-p <pagina>         Usa una pagina diferente para ver anime, 'animeflv' o
                    'monoschinos' por ahora. 'monoschinos' por defecto."""
            )
            sys.exit()
        elif opt in ("-a", "--anime"):
            anime = arg
        elif opt in ("-e", "--episodio"):
            try:
                episode = int(arg)
            except ValueError:
                logger.error("El episodio no puede ser una letra!!!")
                sys.exit(2)
        elif opt in ("-p", "--pagina"):
            if not arg in SITES_LIST:
                logger.error(f"{arg} no esta disponible")
                sys.exit(2)

            anime_site = arg
        elif opt in ("--debug"):
            logger.setLevel(logging.DEBUG)

    if not anime or not episode:
        print("Modo de uso: dolos -a <anime> -e <episodio>")
        sys.exit(2)

    clear_screen()
    watch_anime(anime, episode, anime_site)


def start():
    main(sys.argv[1:])
