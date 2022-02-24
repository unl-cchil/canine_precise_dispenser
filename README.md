# Raspberry Pi controlled precise treat dispenser
**This project provides the source for a precise canine treat dispenser designed for numerical discrimination tasks.**

![Precise Dispenser](https://github.com/unl-cchil/canine_precise_dispenser/blob/main/documentation/figures/Dispenser%20v84_image.png "Precise Dispenser")
### Overview
For detailed overview, review the [user guide](https://github.com/unl-cchil/canine_precise_dispenser/blob/main/documentation/user_guide/unl_cchil_precise_dispenser_guide.pdf).  The basic operating principles of the dispenser can be seen in our [YouTube demo video](https://www.youtube.com/watch?v=fIKlNvzwXUY) or in [this embedded video](https://github.com/unl-cchil/canine_precise_dispenser/blob/main/hardware/dispenser/operation/show_dispenser_video.md).

By using the embedded Python library in the Raspberry Pi image, which is also included in this repository, the stepper motor can be controlled to position the treat holes over the pellet exhaust, leading to a dispensation.  By chaining these events together, a specified quantity of treats can be dispensed.  Additionally, the image is configured with a working build of PsychoPy (v3.2.4).

### Raspberry Pi Image
The SD card image for the Raspberry Pi has all dependencies installed and only needs to have its access point configured using pi-ap.  The image can be found [here](https://drive.google.com/file/d/1r1gbtBNyjnHum-6QpTX6uGOvL8lcQ7Pt/view?usp=sharing).  Use an SD card flasher to write this image to a bootable media, such as balenaEtcher, Win32DiskImager, or other similar software.

### Interfacing Example
```
from precise_dispenser_driver import PreciseDispenser

dispenser = PreciseDispenser()
try:
	dispenser.dispense_treats(10)
	print(“Successfully dispensed ten treats.”)
except ValueError as e:
	print(e)
dispenser.close()
```

### License
The hardware is available under a [CERN-OHL-S-2.0 license](https://spdx.org/licenses/CERN-OHL-S-2.0.html), found [here](https://github.com/unl-cchil/canine_precise_dispenser/blob/main/HWLICENSE.md).

The software is available under an [MIT license](https://opensource.org/licenses/MIT), found [here](https://github.com/unl-cchil/canine_precise_dispenser/blob/main/SWLICENSE.md).

The documentation is available under a [Creative Commons Attribution-ShareAlike 4.0 International Public License (CC BY-SA 4.0)](https://creativecommons.org/licenses/by-sa/4.0/), found [here](https://github.com/unl-cchil/canine_precise_dispenser/blob/main/LICENSE.md).

### Project Mentions
[Hackaday](https://hackaday.com/2022/02/06/open-hardware-dog-treat-dispenser-is-a-stepping-stone-for-behavioral-research/), [UNL Pocket Science](https://news.unl.edu/newsrooms/today/article/lab-s-best-friend-3d-printed-dog-treat-dispenser-outperforms-predecessors/)

### Contact
This project was conducted by the [Canine Cognition and Human Interaction Lab](https://dogcog.unl.edu). For questions, please contact the developer Walker Arce (warce@unomaha.edu) or the principal investigator Jeffrey R. Stevens (jeffrey.r.stevens@gmail.com).

### Citation
Arce, W., and Stevens, J. R. (2022). A precise dispenser design for canine cognition research. _Journal of Open Hardware_, 6(1), 2. http://doi.org/10.5334/joh.41

### Funding
This research was supported by a National Science Foundation grant (SES-1658837) and a University of Nebraska-Lincoln Research Council Grant-in-Aid to JRS.

### Dataset Metadata
The following table is necessary for this dataset to be indexed by search
engines such as <a href="https://g.co/datasetsearch">Google Dataset Search</a>.
<div itemscope itemtype="http://schema.org/Dataset">
<table>
<tr>
<th>property</th>
<th>value</th>
</tr>
<tr>
<td>name</td>
<td><code itemprop="name">A precise dispenser design for canine cognition research reliability testing dataset</code></td>
</tr>
<tr>
<td>description</td>
<td><code itemprop="description">The dataset from the paper [A precise dispenser design for canine cognition research](TBA). We tested five treat dispensers 100 times each with 10 tests of increasing dispensing targets from 1 to 10 treats. Each row of the data file gives the expected and actual number of treats dispensed for a single trial.</code></td>
</tr>
</tr>
<tr>
<td>url</td>
<td><code itemprop="url">https://github.com/unl-cchil/canine_precise_dispenser</code></td>
</tr>
<tr>
<td>sameAs</td>
<td><code itemprop="sameAs">https://github.com/unl-cchil/canine_precise_dispenser</code></td>
</tr>
<tr>
<td>citation</td>
<td><code itemprop="citation">TBA</code></td>
</tr>
<tr>
<td>hw license</td>
<td>
<div itemscope itemtype="http://schema.org/CreativeWork" itemprop="license">
<table>
<tr>
<th>property</th>
<th>value</th>
</tr>
<tr>
<td>name</td>
<td><code itemprop="name">CERN-OHL-S-2.0</code></td>
</tr>
<tr>
<td>url</td>
<td><code itemprop="url">https://spdx.org/licenses/CERN-OHL-S-2.0.html</code></td>
</tr>
</table>
</div>
</td>
</tr>
<tr>
<td>sw license</td>
<td>
<div itemscope itemtype="http://schema.org/CreativeWork" itemprop="license">
<table>
<tr>
<th>property</th>
<th>value</th>
</tr>
<tr>
<td>name</td>
<td><code itemprop="name">MIT</code></td>
</tr>
<tr>
<td>url</td>
<td><code itemprop="url">https://opensource.org/licenses/MIT</code></td>
</tr>
</table>
</div>
</td>
</tr>
<tr>
<td>docs license</td>
<td>
<div itemscope itemtype="http://schema.org/CreativeWork" itemprop="license">
<table>
<tr>
<th>property</th>
<th>value</th>
</tr>
<tr>
<td>name</td>
<td><code itemprop="name">CC BY-SA 4.0</code></td>
</tr>
<tr>
<td>url</td>
<td><code itemprop="url">https://creativecommons.org/licenses/by-sa/4.0/</code></td>
</tr>
</table>
</div>
</td>
</tr>
</table>
</div>
