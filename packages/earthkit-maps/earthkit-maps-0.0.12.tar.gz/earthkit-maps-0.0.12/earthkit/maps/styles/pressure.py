# Copyright 2023, European Centre for Medium Range Weather Forecasts.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from earthkit.maps import styles

MEAN_SEA_LEVEL_PRESSURE_IN_PA = styles.Contour(
    line_colors="#33334d",
    linewidths=[0.5, 0.5, 0.5, 1],
    labels=True,
    level_step=400,
    units="Pa",
    legend_type=None,
)


MEAN_SEA_LEVEL_PRESSURE_IN_HPA = styles.Contour(
    line_colors="#33334d",
    linewidths=[0.5, 0.5, 0.5, 1],
    labels=True,
    level_step=4,
    units="hPa",
    legend_type=None,
)
