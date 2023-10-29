"""
file_handler.py

Filehandler class for PyGPSClient application.

This handles all the file i/o, including:
- binary gnss log file
- json configuration file save, load and validation
- datalog export
- gpx file export
- SPARTN key and crt files

Created on 16 Sep 2020

:author: semuadmin
:copyright: SEMU Consulting © 2020
:license: BSD 3-Clause
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from tkinter import filedialog

from pyubx2 import hextable

from pygpsclient.globals import (
    CONFIGFILE,
    CONFIGNAME,
    FORMAT_BINARY,
    FORMAT_BOTH,
    FORMAT_HEXSTR,
    FORMAT_HEXTAB,
    FORMAT_PARSED,
    GITHUB_URL,
    GPX_NS,
    GPX_TRACK_INTERVAL,
    HOME,
    MAXLOGLINES,
    XML_HDR,
)
from pygpsclient.helpers import set_filename
from pygpsclient.strings import CONFIGTITLE, READTITLE, SAVETITLE


class FileHandler:
    """
    File handler class.
    """

    def __init__(self, app):
        """
        Constructor.

        :param Frame app: reference to main tkinter application
        """

        self.__app = app  # Reference to main application class
        self.__master = self.__app.appmaster  # Reference to root class (Tk)
        self._in_filepath = None
        self._in_filename = None
        self._logpath = None
        self._logname = None
        self._infile = None
        self._logfile = None
        self._trackpath = None
        self._trackname = None
        self._trackfile = None
        self._configpath = None
        self._configfile = None
        self._lines = 0
        self._last_track_update = datetime.fromordinal(1)

    def __del__(self):
        """
        Destructor - close any open files.
        """

        self.close_logfile()
        self.close_trackfile()

    def load_config(self, filename: Path = CONFIGFILE) -> tuple:
        """
        Load configuration file. If filename is not provided, defaults
        to $HOME/pygpsclient.json, otherwise user is prompted for path.

        :param Path filename: fully qualified filename, or None for prompt
        :return: filename, saved settings as dictionary and any error message
        :rtype: tuple
        """

        try:
            if filename is None:
                filename = filedialog.askopenfilename(
                    title=CONFIGTITLE,
                    initialdir=HOME,
                    filetypes=(
                        ("config files", "*.json"),
                        ("all files", "*.*"),
                    ),
                )
                if filename in ((), ""):
                    return (None, None, "cancelled")  # User cancelled

            with open(filename, "r", encoding="utf-8") as jsonfile:
                config = json.load(jsonfile)
                err = self.validate_config(config)
                if err != "":
                    raise ValueError(err)
        except (ValueError, OSError, json.JSONDecodeError) as err:
            return (None, None, str(err))

        return (filename, config, "")

    def validate_config(self, config: dict) -> str:
        """
        Validate configuration file using type designators.

        :param dict config: unvalidated config dict
        :return: error message ("" = valid)
        :rtype: str
        """

        err = ""
        for key, value in config.items():
            ctype = key[-2:]
            valstr = f'"{value}"' if isinstance(value, str) else value
            if ctype == "_n" and not isinstance(value, int):
                err = f"Invalid int value for {key}: {valstr}"
                break
            if ctype == "_f" and not isinstance(value, (int, float)):
                err = f"Invalid float value for {key}: {valstr}"
                break
            if ctype == "_b" and value not in (0, 1):
                err = f"Invalid bool value for {key}: {valstr}"
                break
            if ctype == "_d" and not isinstance(value, dict):
                err = f"Invalid dict value for {key}: {valstr}"
                break
            if ctype == "_l" and not isinstance(value, list):
                err = f"Invalid list value for {key}: {valstr}"
                break
            if ctype == "_t" and not isinstance(value, tuple):
                err = f"Invalid tuple value for {key}: {valstr}"
                break
            if ctype == "_s" and not isinstance(value, str):
                err = f"Invalid str value for {key}: {valstr}"
                break
        return err

    def save_config(self, config: dict, filename: Path = CONFIGFILE) -> str:
        """
        Save configuration file. If filename is not provided, defaults to
        $HOME/pygpsclient.json, otherwise user is prompted for filename.

        :param dict config: configuration settings as dictionary
        :param Path filename: fully qualified path to config file, or None for prompt
        :return: return code "" = success, err str = failure
        :rtype: str
        """

        try:
            if filename is None:
                filename = filedialog.asksaveasfilename(
                    title=CONFIGTITLE,
                    initialdir=HOME,
                    initialfile=f"{CONFIGNAME}.json",
                    filetypes=(
                        ("config files", "*.json"),
                        ("all files", "*.*"),
                    ),
                )
                if filename in ((), ""):
                    return None  # User cancelled

            with open(filename, "w", encoding="utf-8") as file:
                cfgstr = json.dumps(config)
                file.write(cfgstr)
                return ""
        except (OSError, json.JSONDecodeError) as err:
            return str(err)

    def set_logfile_path(self) -> Path:
        """
        Set file path.

        :return: file path
        :rtype: str
        """

        self._logpath = filedialog.askdirectory(
            title=SAVETITLE, initialdir=HOME, mustexist=True
        )
        if self._logpath in ((), ""):
            return None  # User cancelled
        return self._logpath

    def open_logfile(self):
        """
        Open logfile.
        """

        self._lines = 0
        _, self._logname = set_filename(self._logpath, "data", "log")
        self._logfile = open(self._logname, "a+b")

    def open_infile(self) -> Path:
        """
        Open input file for streaming.

        :return: input ile path
        :rtype: str
        """

        self._in_filepath = filedialog.askopenfilename(
            title=READTITLE,
            initialdir=HOME,
            filetypes=(
                ("datalog files", "*.log"),
                ("u-center logs", "*.ubx"),
                ("all files", "*.*"),
            ),
        )
        if self._in_filepath in ((), ""):
            return None  # User cancelled
        return self._in_filepath

    def write_logfile(self, raw_data, parsed_data):
        """
        Append data to log file. Data will be converted to bytes.

        :param data: data to be logged
        """

        if self._logfile is None:
            return

        settings = self.__app.frm_settings.config
        lfm = settings["logformat_s"]
        data = []
        if lfm in (FORMAT_PARSED, FORMAT_BOTH):
            data.append(parsed_data)
        if lfm == FORMAT_BINARY:
            data.append(raw_data)
        if lfm == FORMAT_HEXSTR:
            data.append(raw_data.hex())
        if lfm in (FORMAT_HEXTAB, FORMAT_BOTH):
            data.append(hextable(raw_data))

        for datum in data:
            if not isinstance(datum, bytes):
                datum = (str(datum) + "\r").encode("utf-8")
            try:
                self._logfile.write(datum)
                self._lines += 1
            except ValueError:
                pass

        if self._lines > MAXLOGLINES:
            self.close_logfile()
            self.open_logfile()

    def close_logfile(self):
        """
        Close the logfile.
        """

        try:
            if self._logfile is not None:
                self._logfile.close()
        except IOError:
            pass

    def open_spartnfile(self, ext: str) -> Path:
        """
        Open spartn key / cert files.

        :param str ext: file extension "crt" or "pem"
        :return: spartn file path
        :rtype: str
        """

        filepath = filedialog.askopenfilename(
            title=READTITLE,
            initialdir=HOME,
            filetypes=(
                ("spartn files", f"*.{ext}"),
                ("all files", "*.*"),
            ),
        )
        if filepath in ((), ""):
            return None  # User cancelled
        return filepath

    def open_spartnjson(self) -> Path:
        """
        Open JSON SPARTN config file.

        :return: json file path
        :rtype: str
        """

        filepath = filedialog.askopenfilename(
            title=READTITLE,
            initialdir=HOME,
            filetypes=(
                ("json files", "*.json"),
                ("all files", "*.*"),
            ),
        )
        if filepath in ((), ""):
            return None  # User cancelled
        return filepath

    def set_trackfile_path(self) -> Path:
        """
        Set track directory.

        :return: file path
        :rtype: str
        """

        self._trackpath = filedialog.askdirectory(
            title=SAVETITLE, initialdir=HOME, mustexist=True
        )
        if self._trackpath in ((), ""):
            return None  # User cancelled
        return self._trackpath

    def open_trackfile(self):
        """
        Open track file and create GPX track header tags.
        """

        _, self._trackname = set_filename(self._trackpath, "track", "gpx")
        self._trackfile = open(self._trackname, "a", encoding="utf-8")

        date = datetime.now().isoformat() + "Z"
        gpxtrack = (
            XML_HDR + "<gpx " + GPX_NS + ">"
            "<metadata>"
            f'<link href="{GITHUB_URL}"><text>PyGPSClient</text></link>'
            f"<time>{date}</time>"
            "</metadata>"
            "<trk><name>GPX track from PyGPSClient</name>"
            "<desc>GPX track from PyGPSClient</desc><trkseg>"
        )

        try:
            self._trackfile.write(gpxtrack)
        except ValueError:
            pass

    def add_trackpoint(self, lat: float, lon: float, **kwargs):
        """
        Creates GPX track point from provided parameters.

        :param float lat: latitude
        :param float lon: longitude
        :param kwargs: optional gpx tags as series of key value pairs
        """

        if not (isinstance(lat, (float, int)) and isinstance(lon, (float, int))):
            return

        trkpnt = f'<trkpt lat="{lat}" lon="{lon}">'

        # these are the permissible elements in the GPX schema for wptType
        # http://www.topografix.com/GPX/1/1/#type_wptType
        for tag in (
            "ele",
            "time",
            "magvar",
            "geoidheight",
            "name",
            "cmt",
            "desc",
            "src",
            "link",
            "sym",
            "type",
            "fix",
            "sat",
            "hdop",
            "vdop",
            "pdop",
            "ageofdgpsdata",
            "dgpsid",
            "extensions",
        ):
            if tag in kwargs:
                val = kwargs[tag]
                trkpnt += f"<{tag}>{val}</{tag}>"

        trkpnt += "</trkpt>"

        try:
            self._trackfile.write(trkpnt)
        except (IOError, ValueError):
            pass

    def close_trackfile(self):
        """
        Create GPX track trailer tags and close track file.
        """

        gpxtrack = "</trkseg></trk></gpx>"
        try:
            if self._trackfile is not None:
                self._trackfile.write(gpxtrack)
                self._trackfile.close()
        except (IOError, ValueError):
            pass

    def update_gpx_track(self):
        """
        Update GPX track with latest valid position readings.
        """

        gnss_status = self.__app.gnss_status
        # must have valid coords (apologies if you live on Null Island)
        if (
            isinstance(gnss_status.lat, str)
            or isinstance(gnss_status.lon, str)
            or (gnss_status.lat == 0 and gnss_status.lon == 0)
        ):
            return

        if datetime.now() > self._last_track_update + timedelta(
            seconds=GPX_TRACK_INTERVAL
        ):
            today = datetime.now()
            gpstime = gnss_status.utc
            trktime = datetime(
                today.year,
                today.month,
                today.day,
                gpstime.hour,
                gpstime.minute,
                gpstime.second,
                gpstime.microsecond,
            )
            time = f"{trktime.isoformat()}Z"
            if gnss_status.diff_corr:
                fix = "dgps"
            elif gnss_status.fix == "3D":
                fix = "3d"
            elif gnss_status.fix == "2D":
                fix = "2d"
            else:
                fix = "none"
            diff_age = gnss_status.diff_age
            diff_station = gnss_status.diff_station
            if diff_age in [None, "", 0] or diff_station in [None, "", 0]:
                self.add_trackpoint(
                    gnss_status.lat,
                    gnss_status.lon,
                    ele=gnss_status.alt,
                    time=time,
                    fix=fix,
                    sat=gnss_status.sip,
                    pdop=gnss_status.pdop,
                )
            else:
                self.add_trackpoint(
                    gnss_status.lat,
                    gnss_status.lon,
                    ele=gnss_status.alt,
                    time=time,
                    fix=fix,
                    sat=gnss_status.sip,
                    pdop=gnss_status.pdop,
                    ageofdgpsdata=diff_age,
                    dgpsid=diff_station,
                )

            self._last_track_update = datetime.now()
