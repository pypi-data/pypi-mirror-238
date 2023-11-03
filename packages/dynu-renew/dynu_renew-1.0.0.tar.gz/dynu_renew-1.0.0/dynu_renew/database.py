"""dynu_renew.database file."""

from os.path import join
from sqlite3 import connect


class Database:
    """Database class."""

    __con = None
    __cur = None

    def __init__(self):
        """Database constructor."""

    def __enter__(self):
        """Database enter."""
        self.__con = connect(join('instance', 'dynu-renew.db'))
        self.__cur = self.__con.cursor()

        self.__cur.execute('CREATE TABLE IF NOT EXISTS dynu(domain VARCHAR(256) PRIMARY KEY, ip VARCHAR(15));')

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Database exit."""
        self.__con.close()

    def check_domain_ip(self, domain: str, ip: str) -> bool:
        """Check domain IP.

        :param domain: Referring domain.
        :type ip: str
        :param ip: IP to compare with saved IP.
        :type ip: str
        :return: True if passed IP is equal to saved IP, else False.
        :rtype: bool
        """
        return self.__cur.execute(
            f'SELECT ip FROM dynu WHERE domain = \'{domain}\' AND ip = \'{ip}\';'
        ).fetchone() is not None

    def save_domain_ip(self, domain: str, ip: str):
        """Save domain IP.

        :param domain: Referring domain.
        :type ip: str
        :param ip: IP to save.
        :type ip: str
        """
        self.__cur.execute(
            f'INSERT INTO dynu(domain, ip) VALUES(\'{domain}\', \'{ip}\') '
            f'ON CONFLICT(domain) DO UPDATE SET ip = \'{ip}\';'
        )
        self.__con.commit()
