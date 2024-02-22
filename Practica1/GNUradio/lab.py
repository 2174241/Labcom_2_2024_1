#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#
# SPDX-License-Identifier: GPL-3.0
#
# GNU Radio Python Flow Graph
# Title: Promediador
# Author: xd
# GNU Radio version: 3.9.8.0

from distutils.version import StrictVersion

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print("Warning: failed to XInitThreads()")

from PyQt5 import Qt
from gnuradio import qtgui
import sip
from gnuradio import blocks
from gnuradio import gr
from gnuradio.filter import firdes
from gnuradio.fft import window
import sys
import signal
from argparse import ArgumentParser
from gnuradio.eng_arg import eng_float, intx
from gnuradio import eng_notation
import lab_epy_block_1 as epy_block_1  # embedded python block



from gnuradio import qtgui

class lab(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Promediador", catch_exceptions=True)
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Promediador")
        qtgui.util.check_set_qss()
        try:
            self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
            pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "lab")

        try:
            if StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
                self.restoreGeometry(self.settings.value("geometry").toByteArray())
            else:
                self.restoreGeometry(self.settings.value("geometry"))
        except:
            pass

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 32000

        ##################################################
        # Blocks
        ##################################################
        self.rms = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.rms.set_update_time(0.10)
        self.rms.set_title('RMS')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.rms.set_min(i, -1)
            self.rms.set_max(i, 1)
            self.rms.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.rms.set_label(i, "Data {0}".format(i))
            else:
                self.rms.set_label(i, labels[i])
            self.rms.set_unit(i, units[i])
            self.rms.set_factor(i, factor[i])

        self.rms.enable_autoscale(False)
        self._rms_win = sip.wrapinstance(self.rms.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._rms_win)
        self.potencia = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.potencia.set_update_time(0.10)
        self.potencia.set_title('Potencia promedio')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.potencia.set_min(i, -1)
            self.potencia.set_max(i, 1)
            self.potencia.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.potencia.set_label(i, "Data {0}".format(i))
            else:
                self.potencia.set_label(i, labels[i])
            self.potencia.set_unit(i, units[i])
            self.potencia.set_factor(i, factor[i])

        self.potencia.enable_autoscale(False)
        self._potencia_win = sip.wrapinstance(self.potencia.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._potencia_win)
        self.media_cuadratica = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.media_cuadratica.set_update_time(0.10)
        self.media_cuadratica.set_title('Media cuadratica')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.media_cuadratica.set_min(i, -1)
            self.media_cuadratica.set_max(i, 1)
            self.media_cuadratica.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.media_cuadratica.set_label(i, "Data {0}".format(i))
            else:
                self.media_cuadratica.set_label(i, labels[i])
            self.media_cuadratica.set_unit(i, units[i])
            self.media_cuadratica.set_factor(i, factor[i])

        self.media_cuadratica.enable_autoscale(False)
        self._media_cuadratica_win = sip.wrapinstance(self.media_cuadratica.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._media_cuadratica_win)
        self.media = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.media.set_update_time(0.10)
        self.media.set_title('Media')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.media.set_min(i, -1)
            self.media.set_max(i, 1)
            self.media.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.media.set_label(i, "Data {0}".format(i))
            else:
                self.media.set_label(i, labels[i])
            self.media.set_unit(i, units[i])
            self.media.set_factor(i, factor[i])

        self.media.enable_autoscale(False)
        self._media_win = sip.wrapinstance(self.media.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._media_win)
        self.epy_block_1 = epy_block_1.blk()
        self.desviacion = qtgui.number_sink(
            gr.sizeof_float,
            0,
            qtgui.NUM_GRAPH_HORIZ,
            1,
            None # parent
        )
        self.desviacion.set_update_time(0.10)
        self.desviacion.set_title('Desviacion estandar')

        labels = ['', '', '', '', '',
            '', '', '', '', '']
        units = ['', '', '', '', '',
            '', '', '', '', '']
        colors = [("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"),
            ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black"), ("black", "black")]
        factor = [1, 1, 1, 1, 1,
            1, 1, 1, 1, 1]

        for i in range(1):
            self.desviacion.set_min(i, -1)
            self.desviacion.set_max(i, 1)
            self.desviacion.set_color(i, colors[i][0], colors[i][1])
            if len(labels[i]) == 0:
                self.desviacion.set_label(i, "Data {0}".format(i))
            else:
                self.desviacion.set_label(i, labels[i])
            self.desviacion.set_unit(i, units[i])
            self.desviacion.set_factor(i, factor[i])

        self.desviacion.enable_autoscale(False)
        self._desviacion_win = sip.wrapinstance(self.desviacion.qwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._desviacion_win)
        self.blocks_vector_source_x_0 = blocks.vector_source_f((1, 2, -1), True, 1, [])


        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_vector_source_x_0, 0), (self.epy_block_1, 0))
        self.connect((self.epy_block_1, 4), (self.desviacion, 0))
        self.connect((self.epy_block_1, 0), (self.media, 0))
        self.connect((self.epy_block_1, 1), (self.media_cuadratica, 0))
        self.connect((self.epy_block_1, 3), (self.potencia, 0))
        self.connect((self.epy_block_1, 2), (self.rms, 0))


    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "lab")
        self.settings.setValue("geometry", self.saveGeometry())
        self.stop()
        self.wait()

        event.accept()

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate




def main(top_block_cls=lab, options=None):

    if StrictVersion("4.5.0") <= StrictVersion(Qt.qVersion()) < StrictVersion("5.0.0"):
        style = gr.prefs().get_string('qtgui', 'style', 'raster')
        Qt.QApplication.setGraphicsSystem(style)
    qapp = Qt.QApplication(sys.argv)

    tb = top_block_cls()

    tb.start()

    tb.show()

    def sig_handler(sig=None, frame=None):
        tb.stop()
        tb.wait()

        Qt.QApplication.quit()

    signal.signal(signal.SIGINT, sig_handler)
    signal.signal(signal.SIGTERM, sig_handler)

    timer = Qt.QTimer()
    timer.start(500)
    timer.timeout.connect(lambda: None)

    qapp.exec_()

if __name__ == '__main__':
    main()
