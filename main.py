#
# DBS Project - ue10
# Henning Gütschow
# Niklas Rosseck
# Kilian Woick
#

import sqlite3


def main():
    conn = sqlite3.connect('db/dbs_project.db')
    cursor = conn.cursor()
