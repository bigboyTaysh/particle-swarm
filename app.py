from os import path
from PyQt5 import uic, QtWidgets, QtCore, QtGui
from lib.modules import evolution, test
from lib.models import ThreadClass
import time
import numpy
from PyQt5.QtChart import QChart, QLineSeries, QScatterSeries
import csv
import random

path_to_gui = path.abspath(path.join(path.dirname(__file__), 'gui.ui'))

Form, Window = uic.loadUiType(path_to_gui)
app = QtWidgets.QApplication([])
window = Window()
form = Form()
form.setupUi(window)

chart = QChart()
chart.setBackgroundBrush(QtGui.QColor(41, 43, 47))
form.widget.setChart(chart)
form.widget_animation.setChart(chart)

form.tabWidget.setTabText(0, "Algorytm")
form.tabWidget.setTabText(1, "Testy")
window.show()

draw_thread = ThreadClass()

def run_evolution():
    range_a = float(str(form.input_a.text()))
    range_b = float(str(form.input_b.text()))
    precision = int(str(form.input_d.text()))
    particles_number = int(str(form.input_particles.text()))
    iterations = int(str(form.input_iterations.text()))
    c1_weight = float(str(form.input_c1.text()))
    c2_weight = float(str(form.input_c2.text()))
    c3_weight = float(str(form.input_c3.text()))
    neighborhood_distance = float(str(form.input_neighborhood.text()))

    app.setOverrideCursor(QtCore.Qt.WaitCursor)

    best_real, best_fx, best_fxs, avg_fxs, min_fxs, particles = evolution(
        range_a, range_b, precision, particles_number, iterations, c1_weight, c2_weight, c3_weight, neighborhood_distance)

    chart = QChart()
    bests = QLineSeries() 
    avg = QLineSeries() 
    mins = QLineSeries() 

    pen_best = bests.pen()
    pen_best.setWidth(1)
    pen_best.setBrush(QtGui.QColor("red"))

    pen_avg = avg.pen()
    pen_avg.setWidth(1)
    pen_avg.setBrush(QtGui.QColor("green"))

    pen_min = mins.pen()
    pen_min.setWidth(1)
    pen_min.setBrush(QtGui.QColor("blue"))

    bests.setPen(pen_best)
    avg.setPen(pen_avg)
    mins.setPen(pen_min)

    form.best_table.item(1,0).setText(str(best_real))
    form.best_table.item(1,1).setText(str(best_fx))

    for i in range(len(best_fxs)):
        bests.append(i+1, best_fxs[i])
        avg.append(i+1, avg_fxs[i])
        mins.append(i+1, min_fxs[i])

    chart.addSeries(bests)
    chart.addSeries(avg)
    chart.addSeries(mins)

    chart.setBackgroundBrush(QtGui.QColor(41, 43, 47))
    chart.createDefaultAxes()
    chart.legend().hide()
    chart.setContentsMargins(-10, -10, -10, -10)
    chart.layout().setContentsMargins(0, 0, 0, 0)
    chart.axisX().setTickCount(11)
    chart.axisX().setLabelsColor(QtGui.QColor("white"))
    chart.axisX().setGridLineColor(QtGui.QColor("grey"))
    chart.axisX().setLabelFormat("%i")
    chart.axisY().setRange(-2,2)
    chart.axisY().setLabelsColor(QtGui.QColor("white"))
    chart.axisY().setGridLineColor(QtGui.QColor("grey"))
    form.widget.setChart(chart)

    draw_thread.particles_list = particles
    draw_thread.start()

    app.restoreOverrideCursor()


def update_particles(particles):
    animation_chart = QChart()
    reals = QScatterSeries()

    pen_reals = reals.pen()
    pen_reals.setBrush(QtGui.QColor("white"))
    reals.setMarkerSize(5)
    reals.setColor(QtGui.QColor("red"))
    reals.setPen(pen_reals)

    for particle in particles:
        reals.append(particle, 0)
        
    animation_chart.addSeries(reals)
    animation_chart.setBackgroundBrush(QtGui.QColor(41, 43, 47))
    animation_chart.createDefaultAxes()
    animation_chart.legend().hide()
    animation_chart.setContentsMargins(-10, -10, -10, -10)
    animation_chart.layout().setContentsMargins(0, 0, 0, 0)
    animation_chart.axisX().setTickCount(17)
    animation_chart.axisY().setTickCount(3)
    animation_chart.axisX().setLabelsColor(QtGui.QColor("white"))
    animation_chart.axisX().setGridLineColor(QtGui.QColor("grey"))
    animation_chart.axisX().setRange(-4,12)
    animation_chart.axisY().setRange(-1,1)
    animation_chart.axisY().setLabelsColor(QtGui.QColor("white"))
    animation_chart.axisY().setGridLineColor(QtGui.QColor("grey"))
    form.widget_animation.setChart(animation_chart)
    


def run_test():
    range_a = float(str(form.input_a_test.text()))
    range_b = float(str(form.input_b_test.text()))
    precision = int(str(form.input_d_test.text()))

    app.setOverrideCursor(QtCore.Qt.WaitCursor)
    start = time.time()
    results  = test(range_a, range_b, precision)
    print(time.time() - start)
    app.restoreOverrideCursor()

    chart = QChart()
    series = QLineSeries()

    form.test_table.setRowCount(0)

    form.test_table.insertRow(0)
    item = QtWidgets.QTableWidgetItem("cząsteczki")
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    form.test_table.setItem(0, 0, item)

    item = QtWidgets.QTableWidgetItem("iteracje")
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    form.test_table.setItem(0, 1, item)

    item = QtWidgets.QTableWidgetItem("c1")
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    form.test_table.setItem(0, 2, item)

    item = QtWidgets.QTableWidgetItem("c2")
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    form.test_table.setItem(0, 3, item)

    item = QtWidgets.QTableWidgetItem("c3")
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    form.test_table.setItem(0, 4, item)

    item = QtWidgets.QTableWidgetItem("sąsiedztwo")
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    form.test_table.setItem(0, 5, item)

    item = QtWidgets.QTableWidgetItem("fmax")
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    form.test_table.setItem(0, 6, item)

    item = QtWidgets.QTableWidgetItem("favg")
    item.setTextAlignment(QtCore.Qt.AlignCenter)
    form.test_table.setItem(0, 7, item)

    sorted_list = sorted(results, key=lambda x: x.fave, reverse=True)

    for i in range(0, len(sorted_list)):
        form.test_table.insertRow(i+1)
        form.test_table.setItem(i+1, 0, QtWidgets.QTableWidgetItem(str(sorted_list[i].particles)))
        form.test_table.setItem(i+1, 1, QtWidgets.QTableWidgetItem(str(sorted_list[i].iterations)))
        form.test_table.setItem(i+1, 2, QtWidgets.QTableWidgetItem(str(sorted_list[i].c1)))
        form.test_table.setItem(i+1, 3, QtWidgets.QTableWidgetItem(str(sorted_list[i].c2)))
        form.test_table.setItem(i+1, 4, QtWidgets.QTableWidgetItem(str(sorted_list[i].c3)))
        form.test_table.setItem(i+1, 5, QtWidgets.QTableWidgetItem(str(sorted_list[i].neighborhood)))
        form.test_table.setItem(i+1, 6, QtWidgets.QTableWidgetItem(str(sorted_list[i].fmax)))
        form.test_table.setItem(i+1, 7, QtWidgets.QTableWidgetItem(str(sorted_list[i].fave)))


draw_thread.signal.connect(update_particles)
form.button_start.clicked.connect(run_evolution)
form.button_test.clicked.connect(run_test)
app.exec()
