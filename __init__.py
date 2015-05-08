# -*- coding: utf-8 -*-
"""
/***************************************************************************
 relocator
                                 A QGIS plugin
 relocates all your project data to a specific location
                             -------------------
        begin                : 2015-05-01
        copyright            : (C) 2015 by Riccardo Klinger / Geolicious
        email                : riccardo.klinger@geolicious.de
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load relocator class from file relocator.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .relocator import relocator
    return relocator(iface)
