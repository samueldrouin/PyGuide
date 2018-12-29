# This file is part of PyGuide.
#
# PyGuide is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# PyGuide is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with PyGuide.  If not, see <http://www.gnu.org/licenses/>.

"""
This module contains the function that execute all SQLite query
"""

# PyQt import
from PyQt5.QtCore import QFile, QIODevice, QTextStream
from PyQt5.QtSql import QSqlQuery

# Project import
import guide.rc_query
from guide.script.database import database_error


def execute(q_file, q_values, database):
    """
    Execute the given query with the optionals values

    :param query_file: Query file (from the resources)
    :param query_values: Dict of the query values {Identifier: Value}
    :return: Query output
    """

    # Read the query
    file = QFile(q_file)
    file.open(QIODevice.ReadOnly | QFile.Text)
    query_str = QTextStream(file).readAll()
    file.close()

    # Prepare the query
    query = QSqlQuery(database)
    query.prepare(query_str)

    if q_values:
        for key, value in q_values.items():
            query.bindValue(':{}'.format(key), value)

    # Execute the query
    query.exec_()

    if not database_error.sql_error_handler(query.lastError()):
        return True, query
    return False, query
