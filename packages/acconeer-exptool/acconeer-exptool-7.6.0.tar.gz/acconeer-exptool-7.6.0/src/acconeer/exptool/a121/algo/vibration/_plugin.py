# Copyright (c) Acconeer AB, 2023
# All rights reserved

from __future__ import annotations

import logging
from enum import Enum, auto
from typing import Callable, Optional, Type

import numpy as np

import pyqtgraph as pg

import acconeer.exptool as et
from acconeer.exptool import a121
from acconeer.exptool.a121.algo._plugins import (
    ProcessorBackendPluginBase,
    ProcessorBackendPluginSharedState,
    ProcessorPluginPreset,
    ProcessorViewPluginBase,
    SetupMessage,
)
from acconeer.exptool.a121.algo._utils import APPROX_BASE_STEP_LENGTH_M
from acconeer.exptool.a121.algo.vibration import (
    Processor,
    ProcessorConfig,
    ProcessorResult,
    get_sensor_config,
)
from acconeer.exptool.app.new import (
    AppModel,
    Message,
    PgPlotPlugin,
    PidgetFactoryMapping,
    PluginFamily,
    PluginGeneration,
    PluginPresetBase,
    PluginSpecBase,
    backend,
    pidgets,
)


log = logging.getLogger(__name__)


class PluginPresetId(Enum):
    DEFAULT = auto()


class BackendPlugin(ProcessorBackendPluginBase[ProcessorConfig, ProcessorResult]):

    PLUGIN_PRESETS = {
        PluginPresetId.DEFAULT.value: lambda: ProcessorPluginPreset(
            session_config=a121.SessionConfig(get_sensor_config()),
            processor_config=BackendPlugin.get_processor_config_cls()(),
        ),
    }

    @classmethod
    def get_processor(cls, state: ProcessorBackendPluginSharedState[ProcessorConfig]) -> Processor:
        if state.metadata is None:
            raise RuntimeError("metadata is None")

        if isinstance(state.metadata, list):
            raise RuntimeError("metadata is unexpectedly extended")

        return Processor(
            sensor_config=state.session_config.sensor_config,
            processor_config=state.processor_config,
            metadata=state.metadata,
        )

    @classmethod
    def get_processor_config_cls(cls) -> Type[ProcessorConfig]:
        return ProcessorConfig

    @classmethod
    def get_default_sensor_config(cls) -> a121.SensorConfig:
        return get_sensor_config()


class ViewPlugin(ProcessorViewPluginBase[ProcessorConfig]):
    @classmethod
    def get_pidget_mapping(cls) -> PidgetFactoryMapping:
        # Note: Incomplete mapping
        return {
            "time_series_length": pidgets.IntPidgetFactory(
                name_label_text="Time series length:",
                limits=(0, None),
            ),
            "lp_coeff": pidgets.FloatSliderPidgetFactory(
                name_label_text="Time filtering coefficient:",
                suffix="",
                limits=(0, 1),
                decimals=2,
            ),
            "sensitivity": pidgets.FloatSliderPidgetFactory(
                name_label_text="Threshold sensitivity:",
                suffix="dB",
                limits=(0, 30),
                decimals=1,
            ),
            "amplitude_threshold": pidgets.FloatPidgetFactory(
                name_label_text="Minimum amplitude:",
                decimals=0,
                limits=(0, None),
            ),
        }

    @classmethod
    def get_processor_config_cls(cls) -> Type[ProcessorConfig]:
        return ProcessorConfig


class PlotPlugin(PgPlotPlugin):
    def __init__(self, app_model: AppModel) -> None:
        super().__init__(app_model=app_model)
        self._plot_job: Optional[ProcessorResult] = None
        self._is_setup = False

    def handle_message(self, message: backend.GeneralMessage) -> None:
        if isinstance(message, backend.PlotMessage):
            self._plot_job = message.result
        elif isinstance(message, SetupMessage):
            if isinstance(message.metadata, list):
                raise RuntimeError("Metadata is unexpectedly extended")

            self.setup(
                metadata=message.metadata,
                sensor_config=message.session_config.sensor_config,
            )
            self._is_setup = True
        else:
            log.warn(f"{self.__class__.__name__} got an unsupported command: {message.name!r}.")

    def draw(self) -> None:
        if not self._is_setup or self._plot_job is None:
            return

        try:
            self.draw_plot_job(processor_result=self._plot_job)
        finally:
            self._plot_job = None

    def setup(self, metadata: a121.Metadata, sensor_config: a121.SensorConfig) -> None:
        self.plot_layout.clear()

        self.meas_dist_m = sensor_config.start_point * APPROX_BASE_STEP_LENGTH_M

        pen = et.utils.pg_pen_cycler(0)
        brush = et.utils.pg_brush_cycler(0)
        brush_dot = et.utils.pg_brush_cycler(1)
        symbol_kw = dict(symbol="o", symbolSize=1, symbolBrush=brush, symbolPen="k")
        feat_kw = dict(pen=pen, **symbol_kw)
        symbol_dot_kw = dict(symbol="o", symbolSize=10, symbolBrush=brush_dot, symbolPen="k")

        # presence plot
        self.presence_plot = pg.PlotItem()
        self.presence_plot.setMenuEnabled(False)
        self.presence_plot.showGrid(x=False, y=True)
        self.presence_plot.setLabel("left", "Max amplitude")
        self.presence_plot.setLabel("bottom", "Distance (m)")
        self.presence_plot.setXRange(self.meas_dist_m - 0.001, self.meas_dist_m + 0.001)
        self.presence_curve = self.presence_plot.plot(**dict(pen=pen, **symbol_dot_kw))

        self.presence_threshold = pg.InfiniteLine(pen=pen, angle=0)
        self.presence_plot.addItem(self.presence_threshold)
        self.presence_threshold.show()

        self.smooth_max_presence = et.utils.SmoothMax(tau_decay=10.0)

        # sweep and threshold plot
        self.time_series_plot = pg.PlotItem()
        self.time_series_plot.setMenuEnabled(False)
        self.time_series_plot.showGrid(x=True, y=True)
        self.time_series_plot.setLabel("left", "Displacement (mm)")
        self.time_series_plot.setLabel("bottom", "History")
        self.time_series_curve = self.time_series_plot.plot(**feat_kw)

        sublayout = self.plot_layout.addLayout(row=0, col=0)
        sublayout.layout.setColumnStretchFactor(1, 5)
        sublayout.addItem(self.presence_plot, row=0, col=0)
        sublayout.addItem(self.time_series_plot, row=0, col=1)

        self.smooth_lim_time_series = et.utils.SmoothLimits(tau_decay=0.5, tau_grow=0.1)

        self.fft_plot = self.plot_layout.addPlot(col=0, row=1)
        self.fft_plot.setMenuEnabled(False)
        self.fft_plot.showGrid(x=True, y=True)
        self.fft_plot.setLabel("left", "Power (dB)")
        self.fft_plot.setLabel("bottom", "Frequency (Hz)")
        self.fft_plot.addItem(pg.PlotDataItem())
        self.fft_curve = [
            self.fft_plot.plot(**feat_kw),
            self.fft_plot.plot(**dict(pen=pen, **symbol_dot_kw)),
        ]

        self.text_item = pg.TextItem(
            fill=pg.mkColor(0xFF, 0x7F, 0x0E, 200),
            anchor=(0.5, 0),
        )
        self.text_item.hide()
        self.fft_plot.addItem(self.text_item)

        self.smooth_max_fft = et.utils.SmoothMax()

    def draw_plot_job(self, processor_result: ProcessorResult) -> None:

        time_series = processor_result.time_series
        z_abs_db = processor_result.lp_z_abs_db
        freqs = processor_result.freqs
        max_amplitude = processor_result.max_amplitude
        amplitude_threshold = processor_result.amplitude_threshold
        max_psd_ampl = processor_result.max_psd_ampl
        max_psd_ampl_freq = processor_result.max_psd_ampl_freq

        # plot object presence metric.
        self.presence_curve.setData([self.meas_dist_m], [max_amplitude])
        self.presence_threshold.setValue(amplitude_threshold)
        lim = self.smooth_max_presence.update(max_amplitude)
        self.presence_plot.setYRange(0, max(1000.0, lim))

        if processor_result.result_available:
            # plot time series and psd as object is present.
            self.time_series_curve.setData(time_series)
            lim = self.smooth_lim_time_series.update(time_series)
            self.time_series_plot.setYRange(lim[0], lim[1])

            assert z_abs_db is not None
            self.fft_curve[0].setData(freqs, z_abs_db)
            lim = self.smooth_max_fft.update(np.max(z_abs_db))
            self.fft_plot.setYRange(0, lim)

            if max_psd_ampl_freq is not None:
                self.fft_curve[1].setData([max_psd_ampl_freq], [max_psd_ampl])
                # Place text box centered at the top of the plotting window.
                self.text_item.setPos(max(freqs) / 2, lim * 0.95)
                html_format = (
                    '<div style="text-align: center">'
                    '<span style="color: #FFFFFF;font-size:15pt;">'
                    "{}</span></div>".format("Detected Frequency: " + str(int(max_psd_ampl_freq)))
                )
                self.text_item.setHtml(html_format)
                self.text_item.show()
            else:
                self.fft_curve[1].setData([], [])
                self.text_item.hide()


class PluginSpec(PluginSpecBase):
    def create_backend_plugin(
        self, callback: Callable[[Message], None], key: str
    ) -> BackendPlugin:
        return BackendPlugin(callback=callback, generation=self.generation, key=key)

    def create_view_plugin(self, app_model: AppModel) -> ViewPlugin:
        return ViewPlugin(app_model=app_model)

    def create_plot_plugin(self, app_model: AppModel) -> PlotPlugin:
        return PlotPlugin(app_model=app_model)


VIBRATION_PLUGIN = PluginSpec(
    generation=PluginGeneration.A121,
    key="vibration",
    title="Vibration measurement",
    description="Quantify the frequency content of vibrating object.",
    family=PluginFamily.EXAMPLE_APP,
    presets=[
        PluginPresetBase(name="Default", preset_id=PluginPresetId.DEFAULT),
    ],
    default_preset_id=PluginPresetId.DEFAULT,
)
