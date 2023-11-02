
import os
import glob
import xarray as xr
import numpy as np
import pandas as pd
from tqdm import tqdm
import datetime
import cftime
import matplotlib.pyplot as plt
from matplotlib import gridspec

from . import utils

class Archive:
    
    def __init__(self, paths, output_dir='./output', load_num=None, settings_csv=None):
        self.paths = paths[:load_num]
        utils.p_header(f'>>> {len(self.paths)} Archive.paths:')
        print(f'Start: {os.path.basename(self.paths[0])}')
        print(f'End: {os.path.basename(self.paths[-1])}')

        ds_all_vars = self.get_ds()
        self.vars = list(ds_all_vars.variables)
        utils.p_success(f'>>> Archive.vars created')
        if 'ncol' in ds_all_vars.dims:
            self.grid = 'SE'
            self.grid_weight = ds_all_vars.area.fillna(0)
            self.grid_dim = 'ncol'
            self.lat = ds_all_vars.lat
        elif 'lat' in ds_all_vars.dims and 'lon' in ds_all_vars.dims:
            self.grid = 'FV'
            self.grid_weight = ds_all_vars.gw.fillna(0)
            self.grid_dim = ('lat', 'lon')
            self.lat = ds_all_vars.lat
        elif 'z_t' in ds_all_vars.dims and 'moc_z' in ds_all_vars.dims:
            self.grid = 'OCN'
            self.grid_weight = ds_all_vars.TAREA.fillna(0)
            self.grid_dim = ('nlat', 'nlon')
            self.lat = ds_all_vars.TLAT
        elif 'ni' in ds_all_vars.dims and 'nj' in ds_all_vars.dims:
            self.grid = 'ICE'
            self.grid_weight = ds_all_vars.tarea.fillna(0)
            self.grid_dim = ('ni', 'nj')
            self.lat = ds_all_vars.TLAT
        else:
            raise ValueError('Unkonwn grid!')

        utils.p_header(f'>>> Archive.grid: {self.grid}')

        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        utils.p_header(f'>>> Archive.output_dir: {self.output_dir}')

        if settings_csv is not None:
            settings_df = pd.read_csv(settings_csv, index_col=0)
            self.settings_csv = settings_csv
            self.settings_df = settings_df
            utils.p_header(f'>>> Archive.settings_csv: {self.settings_csv}')
            utils.p_success(f'>>> Archive.settings_df created')

    def get_ds(self, load_num=1):
        ''' Get a `xarray.Dataset` from a certain file
        '''
        with xr.open_mfdataset(self.paths[:load_num]) as ds:
            return ds

    def slice2series(self, vn=['TS', 'FSNT', 'FLNT', 'LWCF', 'SWCF', 'MOC', 'aice'], load_num=None, account=None, **qsub_kws):
        if type(vn) is not list: vn = [vn]
        vn = list(set(vn) - (set(vn) - set(self.vars)))
        for v in vn:
            name = f'slice2series_{v}'
            pbs_fname = f'pbs_{name}.zsh'
            paths = ''
            for path in self.paths[:load_num]:
                paths += path
                paths += ' '

            output_fpath = os.path.join(self.output_dir, f'{v}.nc')
            if os.path.exists(output_fpath):
                os.remove(output_fpath)

            cmd = f'''
module list > /dev/null 2>&1 || source $LMOD_ROOT/lmod/init/zsh
module --force purge
module load nco
ncrcat -v {v} {paths} {os.path.abspath(output_fpath)}
            '''
            utils.make_pbs(cmd=cmd, name=name, pbs_fname=pbs_fname, account=account, **qsub_kws)
            utils.run_shell(f'qsub {pbs_fname}')
            utils.p_header(f'The output will be located at: {os.path.abspath(output_fpath)}')
    
    def clean_pbs(self):
        utils.run_shell(f'rm -rf *slice2series*')
        
    def clim(self, vn=['aice'], adjust_month=True):
        if type(vn) is not list: vn = [vn]
        vn = list(set(vn) - (set(vn) - set(self.vars)))
        ds = xr.Dataset()
        for v in vn:
            da = xr.open_dataset(os.path.join(self.output_dir, f'{v}.nc'))[v]
            if adjust_month:
                da['time'] = da['time'].get_index('time') - datetime.timedelta(days=1)
            da_clim = da.groupby('time.month').mean()
            ds[v] = da_clim
        return ds

    def clim_gm(self, vn, adjust_month=True):
        ds_clim = self.clim(vn=vn, adjust_month=adjust_month)
        ds = ds_clim.weighted(self.grid_weight).mean(self.grid_dim)
        return ds

    def clim_nhm(self, vn, adjust_month=True):
        ds_clim = self.clim(vn=vn, adjust_month=adjust_month)
        ds = ds_clim.where(self.lat>=0).weighted(self.grid_weight).mean(self.grid_dim)
        return ds

    def clim_shm(self, vn, adjust_month=True):
        ds_clim = self.clim(vn=vn, adjust_month=adjust_month)
        ds = ds_clim.where(self.lat<=0).weighted(self.grid_weight).mean(self.grid_dim)
        return ds

    def ann(self, vn=['TS', 'FSNT', 'FLNT', 'LWCF', 'SWCF', 'MOC', 'aice'], adjust_month=True):
        if type(vn) is not list: vn = [vn]
        vn = list(set(vn) - (set(vn) - set(self.vars)))
        ds = xr.Dataset()
        for v in vn:
            da = xr.open_dataset(os.path.join(self.output_dir, f'{v}.nc'))[v]
            if adjust_month:
                da['time'] = da['time'].get_index('time') - datetime.timedelta(days=1)
            da_ann = utils.monthly2annual(da)
            ds[v] = da_ann
        return ds

    def ann_gm(self, vn, adjust_month=True):
        ds_ann = self.ann(vn=vn, adjust_month=adjust_month)
        ds = ds_ann.weighted(self.grid_weight).mean(self.grid_dim)
        return ds

    def ann_nhm(self, vn, adjust_month=True):
        ds_ann = self.ann(vn=vn, adjust_month=adjust_month)
        ds = ds_ann.where(self.lat>=0).weighted(self.grid_weight).mean(self.grid_dim)
        return ds

    def ann_shm(self, vn, adjust_month=True):
        ds_ann = self.ann(vn=vn, adjust_month=adjust_month)
        ds = ds_ann.where(self.lat<=0).weighted(self.grid_weight).mean(self.grid_dim)
        return ds

    def calc_ts(self, vn=['GMST', 'GMRESTOM', 'GMLWCF', 'GMSWCF', 'NHAICE'], adjust_month=True):
        if type(vn) is not list: vn = [vn]
        vn_map = {
            'GMST': 'TS',
            'GMRESTOM': ('FSNT', 'FLNT'),
            'GMLWCF': 'LWCF',
            'GMSWCF': 'SWCF',
            'NHAICE': 'aice',
        }
        vn_raw = []
        for v in vn_map.values():
            if isinstance(v, (list, tuple)):
                vn_raw.extend(v)
            else:
                vn_raw.append(v)
            
        # remove unavailble variables
        vn_raw = list(set(vn_raw) - (set(vn_raw) - set(self.vars)))
        vn_new = []
        for v in vn:
            if isinstance(vn_map[v], (list, tuple)):
                if set(vn_map[v]) <= set(vn_raw):
                    vn_new.append(v)
            else:
                if vn_map[v] in set(vn_raw):
                    vn_new.append(v)
        vn = vn_new

        ds = xr.Dataset()
        for v in vn:
            if v[:2] == 'GM':
                ds_raw = self.ann_gm(adjust_month=adjust_month, vn=vn_raw)
            elif v[:2] == 'NH':
                ds_raw = self.ann_nhm(adjust_month=adjust_month, vn=vn_raw)
            elif v[:2] == 'SH':
                ds_raw = self.ann_shm(adjust_month=adjust_month, vn=vn_raw)

            if v == 'GMST':
                ds[v] = ds_raw[vn_map[v]] - 273.15
            elif v == 'GMRESTOM':
                ds[v] = ds_raw[vn_map[v][0]] - ds_raw[vn_map[v][1]]
            else:
                ds[v] = ds_raw[vn_map[v]]

        self.diagnostic = ds
        utils.p_success(f'Archive.diagnostic generated with variables: {vn}')

    def plot_ts(self, vn=['GMST', 'GMRESTOM', 'GMLWCF', 'GMSWCF', 'NHAICE'], figsize=[10, 6], ncol=2, wspace=0.3, hspace=0.2, xlim=None, title=None,
                        xlabel='Time [yr]', ylable_dict=None, color_dict=None, ylim_dict=None, ax=None, print_settings=True,
                        prt_setting_list=['cldfrc_rhminl', 'micro_mg_dcs'], **plot_kws):
        # remove unavailable variables
        vn_new = []
        for v in vn:
            if v in self.diagnostic:
                vn_new.append(v)
        vn = vn_new

        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = {}

        nrow = int(np.ceil(len(vn)/ncol))
        gs = gridspec.GridSpec(nrow, ncol)
        gs.update(wspace=wspace, hspace=hspace)

        _ylim_dict = {
            'GMST': (13.5, 15.5),
            'GMRESTOM': (-1, 3),
            'GMLWCF': (24, 26),
            'GMSWCF': (-52, -44),
            'NHAICE': (0, 10),
        }
        if ylim_dict is not None:
            _ylim_dict.update(ylim_dict)

        _ylb_dict = {
            'GMST': r'GMST [$^\circ$C]',
            'GMRESTOM': r'GMRESTOM [W/m$^2$]',
            'GMLWCF': r'GMLWCF [W/m$^2$]',
            'GMSWCF': r'GMSWCF [W/m$^2$]',
            'NHAICE': r'NHAICE [%]',
        }
        if ylable_dict is not None:
            _ylb_dict.update(ylable_dict)

        _clr_dict = {
            'GMST': 'tab:red',
            'GMRESTOM': 'tab:blue',
            'GMLWCF': 'tab:green',
            'GMSWCF': 'tab:orange',
            'NHAICE': 'tab:blue',
        }
        if color_dict is not None:
            _clr_dict.update(color_dict)

        i = 0
        i_row, i_col = 0, 0
        for v in vn:
            if 'fig' in locals():
                ax[v] = fig.add_subplot(gs[i_row, i_col])

            if i_row == nrow-1:
                _xlb = xlabel
            else:
                _xlb = None


            if v == 'GMRESTOM':
                ax[v].axhline(y=0, linestyle='--', color='tab:grey')
            elif v == 'GMLWCF':
                ax[v].axhline(y=25, linestyle='--', color='tab:grey')
            elif v == 'GMSWCF':
                ax[v].axhline(y=-47, linestyle='--', color='tab:grey')
            elif v == 'GMST':
                ax[v].axhline(y=14, linestyle='--', color='tab:grey')

            _plot_kws = {
                'linewidth': 2,
            }
            if plot_kws is not None:
                _plot_kws.update(plot_kws)
            
            ax[v].plot(self.diagnostic[v].time.values, self.diagnostic[v].values, color=_clr_dict[v], **_plot_kws)
            if xlim is not None:
                ax[v].set_xlim(xlim)
            ax[v].set_ylim(_ylim_dict[v])
            ax[v].set_xlabel(_xlb)
            ax[v].set_ylabel(_ylb_dict[v])

            i += 1
            i_col += 1

            if i % 2 == 0:
                i_row += 1

            if i_col == ncol:
                i_col = 0

        if hasattr(self, 'settings_df') and print_settings:
            settings_info = ''
            for name in prt_setting_list:
                nm = f'atm: {name}'
                settings_info += f'{name}: {self.settings_df.loc[nm].values[0].strip()}'
                settings_info += ', '
            settings_info = settings_info[:-2]

        if 'settings_info' in locals():
            if title is None:
                title = settings_info
            else:
                title += f'\n{settings_info}'

                fig.suptitle(title)

        if 'fig' in locals():
            return fig, ax
        else:
            return ax

    def calc_amoc(self, adjust_month=True, vn=['amoc_yz', 'amoc_t']):
        vn_map = {
            'amoc_yz': 'MOC',
            'amoc_t': 'MOC',
        }
        vn_raw = []
        for v in vn:
            if type(vn_map[v]) is list or type(vn_map[v]) is tuple:
                for v_tmp in vn_map[v]:
                    vn_raw.append(v_tmp)
            else:
                vn_raw.append(vn_map[v])

        vn_raw = list(set(vn_raw) - (set(vn_raw) - set(self.vars)))
        ds_raw = self.ann(adjust_month=adjust_month, vn=vn_raw)
        ds_raw['moc_z'] = ds_raw['moc_z']/1e5  # cm -> km
        ds_raw['moc_z'].attrs['units'] = 'km'
        ds = xr.Dataset()
        for v in vn:
            if v == 'amoc_yz':
                ds[v] = ds_raw[vn_map[v]].isel(
                    transport_reg=1, moc_comp=0, time=slice(-30, None),
                ).mean('time').where(ds_raw[vn_map[v]].lat_aux_grid>-35)
            elif v == 'amoc_t':
                ds[v] = ds_raw[vn_map[v]].isel(
                    transport_reg=1, moc_comp=0,
                ).sel(
                    moc_z=slice(0.5, None), lat_aux_grid=slice(28, 90),
                ).max(dim=('moc_z', 'lat_aux_grid'))
            else:
                ds[v] = ds_raw[vn_map[v]]

        self.diagnostic = ds
        utils.p_success(f'Archive.diagnostic generated with variables: {vn}')

    def plot_amoc(self, vn=['amoc_t', 'amoc_yz'], figsize=[10, 4], ncol=2, wspace=0.3, hspace=0.2, title=None,
                        amoc_levels=np.linspace(-24, 24, 25), xlabel_dict=None, ylable_dict=None, ax=None, print_settings=True,
                        prt_setting_list=['cldfrc_rhminl', 'micro_mg_dcs'], amoc_t_xlim=None, amoc_t_ylim=(4, 30), **plot_kws):
        # remove unavailable variables
        vn_new = []
        for v in vn:
            if v in self.diagnostic:
                vn_new.append(v)
        vn = vn_new

        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = {}

        _xlb_dict = {
            'amoc_yz': 'Latitude',
            'amoc_t': 'Time [yr]',
        }
        if xlabel_dict is not None:
            _xlb_dict.update(xlabel_dict)

        _ylb_dict = {
            'amoc_yz': 'Depth [km]',
            'amoc_t': 'AMOC [Sv]',
        }
        if ylable_dict is not None:
            _ylb_dict.update(ylable_dict)

        nrow = int(np.ceil(len(vn)/ncol))
        gs = gridspec.GridSpec(nrow, ncol)
        gs.update(wspace=wspace, hspace=hspace)

        i = 0
        i_row, i_col = 0, 0
        ds = self.diagnostic
        for v in vn:
            if 'fig' in locals():
                ax[v] = fig.add_subplot(gs[i_row, i_col])

            if v == 'amoc_yz':
                im = ax[v].contourf(ds[v].lat_aux_grid, ds[v].moc_z, ds[v], cmap='RdBu_r', extend='both', levels=amoc_levels)
                ax[v].set_xticks([-30, 0, 30, 60, 90])
                ax[v].set_xlim([-35, 90])
                ax[v].invert_yaxis()
                ax[v].set_yticks([0, 2, 4])
                cbar = fig.colorbar(im, extend='both', shrink=0.9, ax=ax[v])
                cbar.ax.set_title('[Sv]')

            elif v == 'amoc_t':
                ax[v].plot(ds[v].time, ds[v])
                ax[v].set_ylim(amoc_t_ylim)
                if amoc_t_xlim is not None:
                    ax[v].set_xlim(amoc_t_xlim)

            ax[v].set_xlabel(_xlb_dict[v])
            ax[v].set_ylabel(_ylb_dict[v])
            _plot_kws = {
                'linewidth': 2,
            }
            if plot_kws is not None:
                _plot_kws.update(plot_kws)

            i += 1
            i_col += 1

            if i % 2 == 0:
                i_row += 1

            if i_col == ncol:
                i_col = 0

        if hasattr(self, 'settings_df') and print_settings:
            settings_info = ''
            for name in prt_setting_list:
                nm = f'atm: {name}'
                settings_info += f'{name}: {self.settings_df.loc[nm].values[0].strip()}'
                settings_info += ', '
            settings_info = settings_info[:-2]

        if 'settings_info' in locals():
            if title is None:
                title = settings_info
            else:
                title += f'\n{settings_info}'

                fig.suptitle(title)

        if 'fig' in locals():
            return fig, ax
        else:
            return ax

class Archives:
    def __init__(self, archive_dict=None):
        self.archive_dict = archive_dict
        for k, v in self.archive_dict.items():
            v.name = k
    
    def calc_ts(self):
        for k, v in self.archive_dict.items():
            print(f'>>> Processing {k} ...')
            self.archive_dict[k].calc_diagnostic_atm()

    def calc_amoc(self):
        for k, v in self.archive_dict.items():
            print(f'>>> Processing {k} ...')
            self.archive_dict[k].calc_diagnostic_ocn()

    def plot_ts(self, vn=['GMST', 'GMRESTOM', 'GMLWCF', 'GMSWCF', 'NHAICE'], figsize=[10, 6], ncol=2, wspace=0.3, hspace=0.2, xlim=(0, 100), title=None,
                        xlabel='Time [yr]', ylable_dict=None, ylim_dict=None, ax=None, prt_setting_list=['cldfrc_rhminl', 'micro_mg_dcs'], lgd_anchor=(-1, -1.2),
                        plot_list=None, **plot_kws):

        if ax is None:
            fig = plt.figure(figsize=figsize)
            ax = {}

        nrow = int(np.ceil(len(vn)/ncol))
        gs = gridspec.GridSpec(nrow, ncol)
        gs.update(wspace=wspace, hspace=hspace)

        _ylim_dict = {
            'GMST': (13.5, 15.5),
            'GMRESTOM': (-1, 3),
            'GMLWCF': (24, 26),
            'GMSWCF': (-52, -44),
        }
        if ylim_dict is not None:
            _ylim_dict.update(ylim_dict)

        _ylb_dict = {
            'GMST': r'GMST [$^\circ$C]',
            'GMRESTOM': r'GMRESTOM [W/m$^2$]',
            'GMLWCF': r'GMLWCF [W/m$^2$]',
            'GMSWCF': r'GMSWCF [W/m$^2$]',
        }
        if ylable_dict is not None:
            _ylb_dict.update(ylable_dict)

        i = 0
        i_row, i_col = 0, 0
        for v in vn:
            if 'fig' in locals():
                ax[v] = fig.add_subplot(gs[i_row, i_col])

            if i_row == nrow-1:
                _xlb = xlabel
            else:
                _xlb = None


            if v == 'GMRESTOM':
                ax[v].axhline(y=0, linestyle='--', color='tab:grey')
            elif v == 'GMLWCF':
                ax[v].axhline(y=25, linestyle='--', color='tab:grey')
            elif v == 'GMSWCF':
                ax[v].axhline(y=-47, linestyle='--', color='tab:grey')
            elif v == 'GMST':
                ax[v].axhline(y=14, linestyle='--', color='tab:grey')

            _plot_kws = {
                'linewidth': 2,
            }
            if plot_kws is not None:
                _plot_kws.update(plot_kws)
            
            if plot_list is None: plot_list = list(self.archive_dict.keys())
            for k, ar in self.archive_dict.items():
                if k in plot_list:
                    settings_info = ''
                    for name in prt_setting_list:
                        nm = f'atm: {name}'
                        settings_info += f'{name}: {ar.settings_df.loc[nm].values[0].strip()}'
                        settings_info += ', '
                    settings_info = settings_info[:-2]

                    ax[v].plot(ar.diagnostic[v].time.values, ar.diagnostic[v].values, label=settings_info, **_plot_kws)

            ax[v].set_xlim(xlim)
            ax[v].set_ylim(_ylim_dict[v])
            ax[v].set_xlabel(_xlb)
            ax[v].set_ylabel(_ylb_dict[v])

            i += 1
            i_col += 1

            if i % 2 == 0:
                i_row += 1

            if i_col == ncol:
                i_col = 0

        ax[v].legend(loc='lower left', bbox_to_anchor=lgd_anchor)
        if title is not None:
            fig.suptitle(title)

        if 'fig' in locals():
            return fig, ax
        else:
            return ax
            
#     def calc_som_forcings(self, ds_clim, time_name='month', lat_name='TLAT', lon_name='TLONG',
#                               z_name='z_t', hblt_name='HBLT', temp_name='TEMP', salt_name='SALT',
#                               uvel_name='UVEL', vvel_name='VVEL', shf_name='SHF', qflux_name='QFLUX',
#                               anglet_name='ANGLET', region_mask_name='REGION_MASK',
#                               save_path=None, save_format='NETCDF3_CLASSIC'):
#         ''' Calculate the slab ocean forcing

#         Reference: NCL scripts by Jiang Zhu (jiangzhu@ucar.edu) at:  /glade/u/home/jiangzhu/notebooks/pop_frc_mlt.b.e21.B1850.f19_g17.PaleoCalibr.PI.02.ncl
#         '''
#         ds_clim = ds_clim.rename({time_name: 'time', 'nlat': 'nj', 'nlon': 'ni'})
#         ds_clim.coords['time'] = [cftime.DatetimeNoLeap(1,i,1,0,0,0,0, has_year_zero=True) for i in range(1, 13)]

#         hbltin = ds_clim[hblt_name]
#         hblt_avg = hbltin.mean('time')
#         hblttmp = hblt_avg.expand_dims({'time': 12})/100

#         z_t = ds_clim[z_name]
#         zint = (z_t.values[:-1] + z_t.values[1:])/2/100
#         zint = np.insert(zint, 0, 0)
#         zint = np.append(zint, 2*z_t.values[-1]/100-zint[-1])
#         dz = np.diff(zint)

#         xc = ds_clim[lon_name]
#         yc = ds_clim[lat_name]
#         nlat, nlon = xc.shape
#         ntime = 12
#         nz = len(z_t)

#         # calculate weighted T and S
#         wgt = np.empty((ntime, nz, nlat, nlon))
#         for i in range(nz):
#             dz_tmp = hblttmp.values - zint[i]
#             dz_tmp = np.where(dz_tmp < 0, np.nan, dz_tmp)
#             dz_tmp = np.where(dz_tmp > dz[i], dz[i], dz_tmp)
#             dz_tmp = dz_tmp / hblttmp
#             wgt[:,i,:,:] = dz_tmp

#         Ttmp = ds_clim[temp_name]
#         Stmp = ds_clim[salt_name]
#         Ttmp2 = Ttmp * wgt
#         Stmp2 = Stmp * wgt 

#         Tin = Ttmp2.sum(dim=z_name)
#         Sin = Stmp2.sum(dim=z_name)

#         # calculate velocities
#         Utmp = ds_clim[uvel_name][:,0,:,:]
#         Vtmp = ds_clim[vvel_name][:,0,:,:]
#         ang = ds_clim[anglet_name]

#         Utmp2 = Utmp * 0
#         Vtmp2 = Vtmp * 0

#         Utmp2[:,1:,1:] = 0.25*(Utmp[:,1:,1:] + Utmp[:,1:,:-1]+Utmp[:,:-1,1:]+Utmp[:,:-1,:-1])
#         Vtmp2[:,1:,1:] = 0.25*(Vtmp[:,1:,1:] + Vtmp[:,1:,:-1]+Vtmp[:,:-1,1:]+Vtmp[:,:-1,:-1])

#         Uin = (Utmp2*np.cos(ang) + Vtmp2*np.sin(-ang))*0.01
#         Vin = (Vtmp2*np.cos(ang) - Utmp2*np.sin(-ang))*0.01

#         # calculate ocean heat
#         shf = ds_clim[shf_name]
#         qflux = ds_clim[qflux_name]
#         rcp_sw = 1026.*3996.
#         surf = shf+qflux
#         T1 = Tin.values.copy()
#         T1[:-1] = Tin[1:]
#         T1[-1] = Tin[0]
#         T2 = Tin.values.copy()
#         T2[0] = Tin[-1]
#         T2[1:] = Tin[:-1]
#         dT = T1 - T2
#         release = rcp_sw*dT*hblttmp / (86400.*365./6.)
#         ocnheat = surf-release
            
#         # area weighted
#         tarea = ds_clim['TAREA']
#         maskt = np.ones((nlat, nlon))
#         maskt = maskt*(~np.isnan(ocnheat[0,:,:]))
#         err = np.empty(12)
#         for i in range(12):
#             oh_tmp = ocnheat.values[i].flatten()
#             oh_tmp[np.isnan(oh_tmp)] = 0
#             err[i] = np.matmul(oh_tmp,tarea.values.flatten())/np.sum(tarea.values*maskt.values)

#         glob = np.mean(err)
#         ocnheat -= glob

#         # calculate the inverse matrix
#         dhdxin = Tin * 0
#         dhdyin = Tin * 0

#         daysinmo = np.array([31.,28.,31.,30.,31.,30.,31.,31.,30.,31.,30.,31.])
#         xnp = np.copy(daysinmo)
#         xnm = np.copy(daysinmo)

#         xnm[1:] = daysinmo[1:] + daysinmo[:-1]
#         xnm[0] = daysinmo[0] + daysinmo[-1]

#         xnp[:-1] = daysinmo[1:] + daysinmo[:-1]
#         xnp[-1] = daysinmo[0] + daysinmo[-1]

#         aa = 2 * daysinmo / xnm
#         cc = 2 * daysinmo / xnp
#         a = aa / 8.
#         c = cc / 8.
#         b = 1 - a - c

#         M = [
#             [b[0], c[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, a[0]],
#             [a[1], b[1], c[1], 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, a[2], b[2], c[2], 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, a[3], b[3], c[3], 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, a[4], b[4], c[4], 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, a[5], b[5], c[5], 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, a[6], b[6], c[6], 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, a[7], b[7], c[7], 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, a[8], b[8], c[8], 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, a[9], b[9], c[9], 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, a[10], b[10], c[10]],
#             [c[11], 0, 0, 0, 0, 0, 0, 0, 0, 0, a[11], b[11]],
#         ]
#         invM = np.linalg.inv(M)

#         # prepare output vars
#         T = xr.full_like(Tin, 0)
#         S = xr.full_like(Sin, 0)
#         U = xr.full_like(Uin, 0)
#         V = xr.full_like(Vin, 0)
#         dhdx = xr.full_like(dhdxin, 0)
#         dhdy = xr.full_like(dhdyin, 0)
#         hblt = xr.full_like(hbltin, 0)
#         qdp = xr.full_like(shf, 0)

#         for j in range(12):
#             for i in range(12):
#                 T[j] += invM[j, i]*Tin[i]
#                 S[j] += invM[j, i]*Sin[i]
#                 U[j] += invM[j, i]*Uin[i]
#                 V[j] += invM[j, i]*Vin[i]
#                 dhdx[j] += invM[j, i]*dhdxin[i]
#                 dhdy[j] += invM[j, i]*dhdyin[i]
#                 hblt[j] += invM[j, i]*hblttmp[i]
#                 qdp[j] += invM[j, i]*ocnheat[i]

#         ds_out = xr.Dataset()
#         ds_out['time'] = ds_clim['time']
#         ds_out['time'].attrs['long_name'] = 'days since 0001-01-01 00:00:00'
#         ds_out['time'].attrs['units'] = 'observation time'
#         ds_out['time'].attrs['calendar'] = 'noleap'

#         ds_out['xc'] = xc
#         ds_out['xc'].attrs['long_name'] = 'longitude of grid cell center'
#         ds_out['xc'].attrs['units'] = 'degrees east'

#         ds_out['yc'] = yc
#         ds_out['yc'].attrs['long_name'] = 'latitude of grid cell center'
#         ds_out['yc'].attrs['units'] = 'degrees north'

#         ds_out['T'] = T.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['T'].attrs['long_name'] = 'temperature'
#         ds_out['T'].attrs['units'] = 'degC'

#         ds_out['S'] = S.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['S'].attrs['long_name'] = 'salinity'
#         ds_out['S'].attrs['units'] = 'ppt'

#         ds_out['U'] = U.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['U'].attrs['long_name'] = 'u ocean current'
#         ds_out['U'].attrs['units'] = 'm/s'

#         ds_out['V'] = V.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['V'].attrs['long_name'] = 'v ocean current'
#         ds_out['V'].attrs['units'] = 'm/s'

#         ds_out['dhdx'] = dhdx.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['dhdx'].attrs['long_name'] = 'ocean surface slope: zonal'
#         ds_out['dhdx'].attrs['units'] = 'm/m'

#         ds_out['dhdy'] = dhdy.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['dhdy'].attrs['long_name'] = 'ocean surface slope: meridional'
#         ds_out['dhdy'].attrs['units'] = 'm/m'

#         ds_out['hblt'] = hblt.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['hblt'].attrs['long_name'] = 'boundary layer depth'
#         ds_out['hblt'].attrs['units'] = 'm'

#         ds_out['qdp'] = qdp.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['qdp'].attrs['long_name'] = 'ocean heat flux convergence'
#         ds_out['qdp'].attrs['units'] = 'W/m^2'

#         ds_out['area'] = tarea
#         ds_out['area'].attrs['long_name'] = 'area of grid cell in radians squared'
#         ds_out['area'].attrs['units'] = 'area'

#         ds_out['mask'] = ds_clim[region_mask_name]
#         ds_out['mask'].attrs['long_name'] = 'domain maskr'
#         ds_out['mask'].attrs['units'] = 'unitless'

#         ds_out.attrs['title'] = 'Monthly averaged ocean forcing from POP output'
#         ds_out.attrs['conventions'] = 'CCSM data model domain description'
#         ds_out.attrs['source'] = 'cfr.gcm.GCMCase.calc_slab_ocn_forcing (https://github.com/fzhu2e/cfr)'
#         ds_out.attrs['description'] = 'Input data for DOCN7 mixed layer model'
#         ds_out.attrs['note1'] = 'fields computed from 100-yr monthly means from pop'
#         ds_out.attrs['note2'] = 'all fields interpolated to T-grid'
#         ds_out.attrs['note3'] = 'qdp is computed from depth summed ocean column'
#         ds_out.attrs['author'] = 'Feng Zhu (fengzhu@ucar.edu), Jiang Zhu (jiangzhu@ucar.edu)'
#         ds_out.attrs['calendar'] = 'standard'
#         ds_out.attrs['comment'] = 'This data is on the displaced pole grid gx1v7'
#         ds_out.attrs['creation_date'] = datetime.date.today().strftime('%m/%d/%Y')

#         if save_path is not None:
#             ds_out.to_netcdf(save_path, format=save_format)

#         return ds_out

#     def calc_cam_forcings(self, SST, aice, SST_time_name='time', SST_lat_name='TLAT', SST_lon_name='TLONG',
#                           aice_time_name='time', aice_lat_name='TLAT', aice_lon_name='TLON',
#                           save_path=None, save_format='NETCDF3_CLASSIC'):
#         ''' Calculate the forcings for CAM only simulation (F-case)

#         Note that the regridding is implemented by `pyresample` here instead of ESMF.

#         Reference: NCL scripts by Cecile Hannay (hannay@ucar.edu) at: /glade/u/home/hannay/ncl_scripts/sst/B1850_cmip6
#         '''
#         ds_out = xr.Dataset(
#             coords={
#                 'time': SST[SST_time_name],
#                 'lat': np.linspace(-89.5, 89.5, 180),
#                 'lon': np.linspace(0.5, 359.5, 360),
#             }
#         )
#         ds_out['time'].attrs['information'] = 'middle of month'
#         ds_out['time'].attrs['calendar'] = 'gregorian'
#         ds_out['time'].attrs['units'] = 'days since 0001-01-01 00:00:00'

#         ds_out['lat'].attrs['long_name'] = 'latitude'
#         ds_out['lat'].attrs['units'] = 'degrees_north'

#         ds_out['lon'].attrs['long_name'] = 'longitude'
#         ds_out['lon'].attrs['units'] = 'degrees_east'


#         SST_rgd, _, _ = regrid_field_curv_rect(
#             SST.values, SST[SST_lat_name].values, SST[SST_lon_name].values,
#             ds_out.lat.values, ds_out.lon.values)

#         aice_rgd, _, _ = regrid_field_curv_rect(
#             aice.values, aice[aice_lat_name].values, aice[aice_lon_name].values,
#             ds_out.lat.values, ds_out.lon.values)

#         ds_out['SST'] = xr.DataArray(SST_rgd, coords=ds_out.coords)
#         ds_out['SST'].attrs['long_name'] = 'Sea-Surface temperature'
#         ds_out['SST'].attrs['units']     = 'deg_C'

#         ds_out['SEAICE'] = xr.DataArray(aice_rgd*100, coords=ds_out.coords)
#         ds_out['SEAICE'].attrs['long_name'] = 'Sea Ice Concentration'
#         ds_out['SEAICE'].attrs['units']     = '%'

#         # Corrections for data consistency
#         # 1) If SST < -1.8 or ice frac >= 90%, SST = -1.8
#         mask = (ds_out['SST'] < -1.8) | (ds_out['SEAICE'] > 90)
#         ds_out['SST'].values[mask] = -1.8
#         # 2) min ice frac is 0%, max ice_frac is 100%
#         mask = ds_out['SEAICE'] < 0
#         ds_out['SEAICE'].values[mask] = 0
#         mask = ds_out['SEAICE'] > 100
#         ds_out['SEAICE'].values[mask] = 100
#         # 3) No sea ice if SST > 4.97
#         mask = ds_out['SST'] > 4.97
#         ds_out['SEAICE'].values[mask] = 0

#         ds_out['ICEFRAC'] = ds_out['SEAICE'] / 100.

#         if save_path is not None:
#             ds_out.to_netcdf(save_path, format=save_format)

#         return ds_out
        
                

# class GCMCases:
#     ''' The class for postprocessing multiple GCM simulation cases (e.g., CESM)
#     '''
#     def __init__(self, case_dict=None):
#         self.case_dict = case_dict
#         for k, v in self.case_dict.items():
#             v.name = k

#     def calc_atm_gm(self, vars=['GMST', 'GMRESTOM', 'GMLWCF', 'GMSWCF'], verbose=False):
#         for k, v in self.case_dict.items():
#             utils.p_header(f'Processing case: {k} ...')
#             v.calc_atm_gm(vars=vars, verbose=verbose)

#     def plot_ts(self, lgd_kws=None, lgd_idx=1, **plot_kws):
#         _clr_dict = {
#             'GMST': None,
#             'GMRESTOM': None,
#             'GMLWCF': None,
#             'GMSWCF': None,
#         }
#         for k, v in self.case_dict.items():
#             if 'fig' not in locals():
#                 fig, ax = v.plot_ts(color_dict=_clr_dict, label=v.name, **plot_kws)
#             else:
#                 ax = v.plot_ts(ax=ax, color_dict=_clr_dict, label=v.name, **plot_kws)

#         _lgd_kws = {
#             'frameon': False,
#             'loc': 'upper left',
#             'bbox_to_anchor': [1.1, 1],
#         }
#         if lgd_kws is not None:
#             _lgd_kws.update(lgd_kws)

#         vn = list(ax.keys())[lgd_idx]
#         ax[vn].legend(**_lgd_kws)

#         return fig, ax

            

# class GCMCase:
#     ''' The class for postprocessing a GCM simulation case (e.g., CESM)
    
#     Args:
#         dirpath (str): the directory path where the reconstruction results are stored.
#         load_num (int): the number of ensembles to load
#         verbose (bool, optional): print verbose information. Defaults to False.
#     '''

#     def __init__(self, dirpath=None, load_num=None, name=None, include_tags=[], exclude_tags=[], verbose=False):
#         self.fd = {}  # ClimateField
#         self.ts = {}  # EnsTS
#         self.name = name

#         if type(include_tags) is str:
#             include_tags = [include_tags]
#         if type(exclude_tags) is str:
#             exclude_tags = [exclude_tags]

#         if dirpath is not None:
#             fpaths = glob.glob(os.path.join(dirpath, '*.nc'))

#             self.paths = []
#             for path in fpaths:
#                 fname = os.path.basename(path)
#                 include = True

#                 for in_tag in include_tags:
#                     if in_tag not in fname:
#                         include = False

#                 for ex_tag in exclude_tags:
#                     if ex_tag in fname:
#                         include = False

#                 if include:
#                     self.paths.append(path)

#             self.paths = sorted(self.paths)
#             if load_num is not None:
#                 self.paths = self.paths[:load_num]

#         if verbose:
#             utils.p_header(f'>>> {len(self.paths)} GCMCase.paths:')
#             print(self.paths)

#     def get_ds(self, idx=0):
#         ''' Get a `xarray.Dataset` from a certain file
#         '''
#         with xr.open_dataset(self.paths[idx]) as ds:
#             return ds

#     def load(self, vars=None, time_name='time', z_name='z_t', z_val=None,
#              adjust_month=False, mode='timeslice',
#              save_dirpath=None, compress_params=None, verbose=False):
#         ''' Load variables.

#         Args:
#             vars (list): list of variable names.
#             time_name (str): the name of the time dimension.
#             z_name (str): the name of the z dimension (e.g., for ocean output).
#             z_val (float, int, list): the value(s) of the z dimension to pick (e.g., for ocean output).
#             adjust_month (bool): the current CESM version has a bug that the output
#                 has a time stamp inconsistent with the filename with 1 months off, hence
#                 requires an adjustment.
#             verbose (bool, optional): print verbose information. Defaults to False.
#         '''
#         if type(vars) is str:
#             vars = [vars]

#         if mode == 'timeslice':
#             if vars is None:
#                 raise ValueError('Should specify `vars` if mode is "timeslice".')

#             ds_list = []
#             for path in tqdm(self.paths, desc='Loading files'):
#                 with xr.open_dataset(path) as ds_tmp:
#                     ds_list.append(ds_tmp)

#             for vn in vars:
#                 utils.p_header(f'>>> Extracting {vn} ...')
#                 if z_val is None:
#                     da = xr.concat([ds[vn] for ds in ds_list], dim=time_name)
#                 else:
#                     da = xr.concat([ds[vn].sel({z_name: z_val}) for ds in ds_list], dim=time_name)

#                 if adjust_month:
#                     da[time_name] = da[time_name].get_index(time_name) - datetime.timedelta(days=1)

#                 self.fd[vn] = ClimateField(da)

#                 if save_dirpath is not None:
#                     fname = f'{vn}.nc'
#                     save_path = os.path.join(save_dirpath, fname)
#                     self.fd[vn].to_nc(save_path, compress_params=compress_params)

#                 if verbose:
#                     utils.p_success(f'>>> GCMCase.fd["{vn}"] created')

#         elif mode == 'timeseries':
#             for path in self.paths:
#                 fd_tmp = ClimateField().load_nc(path)
#                 vn = fd_tmp.da.name
#                 self.fd[vn] = fd_tmp

#             if verbose:
#                 utils.p_success(f'>>> GCMCase loaded with vars: {list(self.fd.keys())}')

#         else:
#             raise ValueError('Wrong `mode` specified! Options: "timeslice" or "timeseries".')

#     def calc_atm_gm(self, vars=['GMST', 'GMRESTOM', 'GMLWCF', 'GMSWCF'], verbose=False):

#         for vn in vars:
#             if vn == 'GMST':
#                 v = 'TS' if 'TS' in self.fd else 'TREFHT'
#                 gmst = self.fd[v].annualize().geo_mean()
#                 self.ts[vn] = gmst - 273.15

#             elif vn == 'GMRESTOM':
#                 restom = (self.fd['FSNT'] - self.fd['FLNT']).annualize().geo_mean()
#                 self.ts[vn] = restom
            
#             else:
#                 self.ts[vn] = self.fd[vn[2:]].annualize().geo_mean()

#             if verbose:
#                 utils.p_success(f'>>> GCMCase.ts["{vn}"] created')

#     def to_ds(self, mode='ts'):
#         ''' Convert to a `xarray.Dataset`
#         '''
#         da_dict = {}
#         if mode == 'fd':
#             for k, v in self.fd.items():
#                 da_dict[k] = v.da

#         elif mode == 'ts':
#             for k, v in self.ts.items():
#                 time_name = v.time.name
#                 da_dict[k] = xr.DataArray(v.value[:, 0], dims=[time_name], coords={time_name: v.time}, name=k)

#         ds = xr.Dataset(da_dict)
#         if self.name is not None:
#             ds.attrs['casename'] = self.name

#         return ds

#     def to_nc(self, path, mode='ts', verbose=True, compress_params=None):
#         ''' Output the GCM case to a netCDF file.

#         Args:
#             path (str): the path where to save
#         '''
#         _comp_params = {'zlib': True}
#         encoding_dict = {}
#         if compress_params is not None:
#             _comp_params.update(compress_params)

#         if mode == 'fd':
#             for k, v in self.fd.items():
#                 encoding_dict[k] = _comp_params

#         elif mode == 'ts':
#             for k, v in self.ts.items():
#                 encoding_dict[k] = _comp_params

#         try:
#             dirpath = os.path.dirname(path)
#             os.makedirs(dirpath, exist_ok=True)
#         except:
#             pass

#         ds = self.to_ds(mode=mode)

#         if os.path.exists(path):
#             os.remove(path)
            
#         ds.to_netcdf(path, encoding=encoding_dict)
#         if verbose: utils.p_success(f'>>> GCMCase saved to: {path}')

#     def load_nc(self, path, verbose=False):
#         case = GCMCase()
#         ds = xr.open_dataset(path)
#         if 'casename' in ds.attrs:
#             case.name = ds.attrs['casename']

#         for vn in ds.keys():
#             if vn[:2] == 'GM':
#                 case.ts[vn] = EnsTS(time=ds[vn].year, value=ds[vn].values)
#                 if verbose:
#                     utils.p_success(f'>>> GCMCase.ts["{vn}"] created')
#             else:
#                 case.fd[vn] = ClimateField(ds[vn])
#                 if verbose:
#                     utils.p_success(f'>>> GCMCase.fd["{vn}"] created')

#         return case


#     def plot_ts(self, vars=['GMST', 'GMRESTOM', 'GMLWCF', 'GMSWCF'], figsize=[10, 6], ncol=2, wspace=0.3, hspace=0.2, xlim=(0, 100), title=None,
#                     xlabel='Time [yr]', ylable_dict=None, color_dict=None, ylim_dict=None,
#                     ax=None, **plot_kws):

#         if ax is None:
#             fig = plt.figure(figsize=figsize)
#             ax = {}

#         nrow = int(np.ceil(len(vars)/ncol))
#         gs = gridspec.GridSpec(nrow, ncol)
#         gs.update(wspace=wspace, hspace=hspace)

#         _ylim_dict = {
#             'GMST': (13.5, 15.5),
#             'GMRESTOM': (-1, 3),
#             'GMLWCF': (24, 26),
#             'GMSWCF': (-54, -44),
#         }
#         if ylim_dict is not None:
#             _ylim_dict.update(ylim_dict)

#         _ylb_dict = {
#             'GMST': r'GMST [$^\circ$C]',
#             'GMRESTOM': r'GMRESTOM [W/m$^2$]',
#             'GMLWCF': r'GMLWCF [W/m$^2$]',
#             'GMSWCF': r'GMSWCF [W/m$^2$]',
#         }
#         if ylable_dict is not None:
#             _ylb_dict.update(ylable_dict)

#         _clr_dict = {
#             'GMST': 'tab:red',
#             'GMRESTOM': 'tab:blue',
#             'GMLWCF': 'tab:green',
#             'GMSWCF': 'tab:orange',
#         }
#         if color_dict is not None:
#             _clr_dict.update(color_dict)

#         i = 0
#         i_row, i_col = 0, 0
#         for k, v in self.ts.items():
#             if 'fig' in locals():
#                 ax[k] = fig.add_subplot(gs[i_row, i_col])

#             if i_row == nrow-1:
#                 _xlb = xlabel
#             else:
#                 _xlb = None


#             if k == 'GMRESTOM':
#                 ax[k].axhline(y=0, linestyle='--', color='tab:grey')
#             elif k == 'GMLWCF':
#                 ax[k].axhline(y=25, linestyle='--', color='tab:grey')
#             elif k == 'GMSWCF':
#                 ax[k].axhline(y=-47, linestyle='--', color='tab:grey')

#             _plot_kws = {
#                 'linewidth': 2,
#             }
#             if plot_kws is not None:
#                 _plot_kws.update(plot_kws)
            

#             v.plot(
#                 ax=ax[k], xlim=xlim, ylim=_ylim_dict[k],
#                 xlabel=_xlb, ylabel=_ylb_dict[k],
#                 color=_clr_dict[k], **_plot_kws,
#             )

#             i += 1
#             i_col += 1

#             if i % 2 == 0:
#                 i_row += 1

#             if i_col == ncol:
#                 i_col = 0

#         if title is not None:
#             fig.suptitle(title)

#         if 'fig' in locals():
#             return fig, ax
#         else:
#             return ax
            
#     def calc_som_forcings(self, ds_clim, time_name='month', lat_name='TLAT', lon_name='TLONG',
#                               z_name='z_t', hblt_name='HBLT', temp_name='TEMP', salt_name='SALT',
#                               uvel_name='UVEL', vvel_name='VVEL', shf_name='SHF', qflux_name='QFLUX',
#                               anglet_name='ANGLET', region_mask_name='REGION_MASK',
#                               save_path=None, save_format='NETCDF3_CLASSIC'):
#         ''' Calculate the slab ocean forcing

#         Reference: NCL scripts by Jiang Zhu (jiangzhu@ucar.edu) at:  /glade/u/home/jiangzhu/notebooks/pop_frc_mlt.b.e21.B1850.f19_g17.PaleoCalibr.PI.02.ncl
#         '''
#         ds_clim = ds_clim.rename({time_name: 'time', 'nlat': 'nj', 'nlon': 'ni'})
#         ds_clim.coords['time'] = [cftime.DatetimeNoLeap(1,i,1,0,0,0,0, has_year_zero=True) for i in range(1, 13)]

#         hbltin = ds_clim[hblt_name]
#         hblt_avg = hbltin.mean('time')
#         hblttmp = hblt_avg.expand_dims({'time': 12})/100

#         z_t = ds_clim[z_name]
#         zint = (z_t.values[:-1] + z_t.values[1:])/2/100
#         zint = np.insert(zint, 0, 0)
#         zint = np.append(zint, 2*z_t.values[-1]/100-zint[-1])
#         dz = np.diff(zint)

#         xc = ds_clim[lon_name]
#         yc = ds_clim[lat_name]
#         nlat, nlon = xc.shape
#         ntime = 12
#         nz = len(z_t)

#         # calculate weighted T and S
#         wgt = np.empty((ntime, nz, nlat, nlon))
#         for i in range(nz):
#             dz_tmp = hblttmp.values - zint[i]
#             dz_tmp = np.where(dz_tmp < 0, np.nan, dz_tmp)
#             dz_tmp = np.where(dz_tmp > dz[i], dz[i], dz_tmp)
#             dz_tmp = dz_tmp / hblttmp
#             wgt[:,i,:,:] = dz_tmp

#         Ttmp = ds_clim[temp_name]
#         Stmp = ds_clim[salt_name]
#         Ttmp2 = Ttmp * wgt
#         Stmp2 = Stmp * wgt 

#         Tin = Ttmp2.sum(dim=z_name)
#         Sin = Stmp2.sum(dim=z_name)

#         # calculate velocities
#         Utmp = ds_clim[uvel_name][:,0,:,:]
#         Vtmp = ds_clim[vvel_name][:,0,:,:]
#         ang = ds_clim[anglet_name]

#         Utmp2 = Utmp * 0
#         Vtmp2 = Vtmp * 0

#         Utmp2[:,1:,1:] = 0.25*(Utmp[:,1:,1:] + Utmp[:,1:,:-1]+Utmp[:,:-1,1:]+Utmp[:,:-1,:-1])
#         Vtmp2[:,1:,1:] = 0.25*(Vtmp[:,1:,1:] + Vtmp[:,1:,:-1]+Vtmp[:,:-1,1:]+Vtmp[:,:-1,:-1])

#         Uin = (Utmp2*np.cos(ang) + Vtmp2*np.sin(-ang))*0.01
#         Vin = (Vtmp2*np.cos(ang) - Utmp2*np.sin(-ang))*0.01

#         # calculate ocean heat
#         shf = ds_clim[shf_name]
#         qflux = ds_clim[qflux_name]
#         rcp_sw = 1026.*3996.
#         surf = shf+qflux
#         T1 = Tin.values.copy()
#         T1[:-1] = Tin[1:]
#         T1[-1] = Tin[0]
#         T2 = Tin.values.copy()
#         T2[0] = Tin[-1]
#         T2[1:] = Tin[:-1]
#         dT = T1 - T2
#         release = rcp_sw*dT*hblttmp / (86400.*365./6.)
#         ocnheat = surf-release
            
#         # area weighted
#         tarea = ds_clim['TAREA']
#         maskt = np.ones((nlat, nlon))
#         maskt = maskt*(~np.isnan(ocnheat[0,:,:]))
#         err = np.empty(12)
#         for i in range(12):
#             oh_tmp = ocnheat.values[i].flatten()
#             oh_tmp[np.isnan(oh_tmp)] = 0
#             err[i] = np.matmul(oh_tmp,tarea.values.flatten())/np.sum(tarea.values*maskt.values)

#         glob = np.mean(err)
#         ocnheat -= glob

#         # calculate the inverse matrix
#         dhdxin = Tin * 0
#         dhdyin = Tin * 0

#         daysinmo = np.array([31.,28.,31.,30.,31.,30.,31.,31.,30.,31.,30.,31.])
#         xnp = np.copy(daysinmo)
#         xnm = np.copy(daysinmo)

#         xnm[1:] = daysinmo[1:] + daysinmo[:-1]
#         xnm[0] = daysinmo[0] + daysinmo[-1]

#         xnp[:-1] = daysinmo[1:] + daysinmo[:-1]
#         xnp[-1] = daysinmo[0] + daysinmo[-1]

#         aa = 2 * daysinmo / xnm
#         cc = 2 * daysinmo / xnp
#         a = aa / 8.
#         c = cc / 8.
#         b = 1 - a - c

#         M = [
#             [b[0], c[0], 0, 0, 0, 0, 0, 0, 0, 0, 0, a[0]],
#             [a[1], b[1], c[1], 0, 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, a[2], b[2], c[2], 0, 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, a[3], b[3], c[3], 0, 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, a[4], b[4], c[4], 0, 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, a[5], b[5], c[5], 0, 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, a[6], b[6], c[6], 0, 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, a[7], b[7], c[7], 0, 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, a[8], b[8], c[8], 0, 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, a[9], b[9], c[9], 0],
#             [0, 0, 0, 0, 0, 0, 0, 0, 0, a[10], b[10], c[10]],
#             [c[11], 0, 0, 0, 0, 0, 0, 0, 0, 0, a[11], b[11]],
#         ]
#         invM = np.linalg.inv(M)

#         # prepare output vars
#         T = xr.full_like(Tin, 0)
#         S = xr.full_like(Sin, 0)
#         U = xr.full_like(Uin, 0)
#         V = xr.full_like(Vin, 0)
#         dhdx = xr.full_like(dhdxin, 0)
#         dhdy = xr.full_like(dhdyin, 0)
#         hblt = xr.full_like(hbltin, 0)
#         qdp = xr.full_like(shf, 0)

#         for j in range(12):
#             for i in range(12):
#                 T[j] += invM[j, i]*Tin[i]
#                 S[j] += invM[j, i]*Sin[i]
#                 U[j] += invM[j, i]*Uin[i]
#                 V[j] += invM[j, i]*Vin[i]
#                 dhdx[j] += invM[j, i]*dhdxin[i]
#                 dhdy[j] += invM[j, i]*dhdyin[i]
#                 hblt[j] += invM[j, i]*hblttmp[i]
#                 qdp[j] += invM[j, i]*ocnheat[i]

#         ds_out = xr.Dataset()
#         ds_out['time'] = ds_clim['time']
#         ds_out['time'].attrs['long_name'] = 'days since 0001-01-01 00:00:00'
#         ds_out['time'].attrs['units'] = 'observation time'
#         ds_out['time'].attrs['calendar'] = 'noleap'

#         ds_out['xc'] = xc
#         ds_out['xc'].attrs['long_name'] = 'longitude of grid cell center'
#         ds_out['xc'].attrs['units'] = 'degrees east'

#         ds_out['yc'] = yc
#         ds_out['yc'].attrs['long_name'] = 'latitude of grid cell center'
#         ds_out['yc'].attrs['units'] = 'degrees north'

#         ds_out['T'] = T.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['T'].attrs['long_name'] = 'temperature'
#         ds_out['T'].attrs['units'] = 'degC'

#         ds_out['S'] = S.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['S'].attrs['long_name'] = 'salinity'
#         ds_out['S'].attrs['units'] = 'ppt'

#         ds_out['U'] = U.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['U'].attrs['long_name'] = 'u ocean current'
#         ds_out['U'].attrs['units'] = 'm/s'

#         ds_out['V'] = V.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['V'].attrs['long_name'] = 'v ocean current'
#         ds_out['V'].attrs['units'] = 'm/s'

#         ds_out['dhdx'] = dhdx.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['dhdx'].attrs['long_name'] = 'ocean surface slope: zonal'
#         ds_out['dhdx'].attrs['units'] = 'm/m'

#         ds_out['dhdy'] = dhdy.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['dhdy'].attrs['long_name'] = 'ocean surface slope: meridional'
#         ds_out['dhdy'].attrs['units'] = 'm/m'

#         ds_out['hblt'] = hblt.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['hblt'].attrs['long_name'] = 'boundary layer depth'
#         ds_out['hblt'].attrs['units'] = 'm'

#         ds_out['qdp'] = qdp.where(~np.isnan(ds_clim['TEMP'][0,0,:,:]))
#         ds_out['qdp'].attrs['long_name'] = 'ocean heat flux convergence'
#         ds_out['qdp'].attrs['units'] = 'W/m^2'

#         ds_out['area'] = tarea
#         ds_out['area'].attrs['long_name'] = 'area of grid cell in radians squared'
#         ds_out['area'].attrs['units'] = 'area'

#         ds_out['mask'] = ds_clim[region_mask_name]
#         ds_out['mask'].attrs['long_name'] = 'domain maskr'
#         ds_out['mask'].attrs['units'] = 'unitless'

#         ds_out.attrs['title'] = 'Monthly averaged ocean forcing from POP output'
#         ds_out.attrs['conventions'] = 'CCSM data model domain description'
#         ds_out.attrs['source'] = 'cfr.gcm.GCMCase.calc_slab_ocn_forcing (https://github.com/fzhu2e/cfr)'
#         ds_out.attrs['description'] = 'Input data for DOCN7 mixed layer model'
#         ds_out.attrs['note1'] = 'fields computed from 100-yr monthly means from pop'
#         ds_out.attrs['note2'] = 'all fields interpolated to T-grid'
#         ds_out.attrs['note3'] = 'qdp is computed from depth summed ocean column'
#         ds_out.attrs['author'] = 'Feng Zhu (fengzhu@ucar.edu), Jiang Zhu (jiangzhu@ucar.edu)'
#         ds_out.attrs['calendar'] = 'standard'
#         ds_out.attrs['comment'] = 'This data is on the displaced pole grid gx1v7'
#         ds_out.attrs['creation_date'] = datetime.date.today().strftime('%m/%d/%Y')

#         if save_path is not None:
#             ds_out.to_netcdf(save_path, format=save_format)

#         return ds_out

#     def calc_cam_forcings(self, SST, aice, SST_time_name='time', SST_lat_name='TLAT', SST_lon_name='TLONG',
#                           aice_time_name='time', aice_lat_name='TLAT', aice_lon_name='TLON',
#                           save_path=None, save_format='NETCDF3_CLASSIC'):
#         ''' Calculate the forcings for CAM only simulation (F-case)

#         Note that the regridding is implemented by `pyresample` here instead of ESMF.

#         Reference: NCL scripts by Cecile Hannay (hannay@ucar.edu) at: /glade/u/home/hannay/ncl_scripts/sst/B1850_cmip6
#         '''
#         ds_out = xr.Dataset(
#             coords={
#                 'time': SST[SST_time_name],
#                 'lat': np.linspace(-89.5, 89.5, 180),
#                 'lon': np.linspace(0.5, 359.5, 360),
#             }
#         )
#         ds_out['time'].attrs['information'] = 'middle of month'
#         ds_out['time'].attrs['calendar'] = 'gregorian'
#         ds_out['time'].attrs['units'] = 'days since 0001-01-01 00:00:00'

#         ds_out['lat'].attrs['long_name'] = 'latitude'
#         ds_out['lat'].attrs['units'] = 'degrees_north'

#         ds_out['lon'].attrs['long_name'] = 'longitude'
#         ds_out['lon'].attrs['units'] = 'degrees_east'


#         SST_rgd, _, _ = regrid_field_curv_rect(
#             SST.values, SST[SST_lat_name].values, SST[SST_lon_name].values,
#             ds_out.lat.values, ds_out.lon.values)

#         aice_rgd, _, _ = regrid_field_curv_rect(
#             aice.values, aice[aice_lat_name].values, aice[aice_lon_name].values,
#             ds_out.lat.values, ds_out.lon.values)

#         ds_out['SST'] = xr.DataArray(SST_rgd, coords=ds_out.coords)
#         ds_out['SST'].attrs['long_name'] = 'Sea-Surface temperature'
#         ds_out['SST'].attrs['units']     = 'deg_C'

#         ds_out['SEAICE'] = xr.DataArray(aice_rgd*100, coords=ds_out.coords)
#         ds_out['SEAICE'].attrs['long_name'] = 'Sea Ice Concentration'
#         ds_out['SEAICE'].attrs['units']     = '%'

#         # Corrections for data consistency
#         # 1) If SST < -1.8 or ice frac >= 90%, SST = -1.8
#         mask = (ds_out['SST'] < -1.8) | (ds_out['SEAICE'] > 90)
#         ds_out['SST'].values[mask] = -1.8
#         # 2) min ice frac is 0%, max ice_frac is 100%
#         mask = ds_out['SEAICE'] < 0
#         ds_out['SEAICE'].values[mask] = 0
#         mask = ds_out['SEAICE'] > 100
#         ds_out['SEAICE'].values[mask] = 100
#         # 3) No sea ice if SST > 4.97
#         mask = ds_out['SST'] > 4.97
#         ds_out['SEAICE'].values[mask] = 0

#         ds_out['ICEFRAC'] = ds_out['SEAICE'] / 100.

#         if save_path is not None:
#             ds_out.to_netcdf(save_path, format=save_format)

#         return ds_out
        
                

# class GCMCases:
#     ''' The class for postprocessing multiple GCM simulation cases (e.g., CESM)
#     '''
#     def __init__(self, case_dict=None):
#         self.case_dict = case_dict
#         for k, v in self.case_dict.items():
#             v.name = k

#     def calc_atm_gm(self, vars=['GMST', 'GMRESTOM', 'GMLWCF', 'GMSWCF'], verbose=False):
#         for k, v in self.case_dict.items():
#             utils.p_header(f'Processing case: {k} ...')
#             v.calc_atm_gm(vars=vars, verbose=verbose)

#     def plot_ts(self, lgd_kws=None, lgd_idx=1, **plot_kws):
#         _clr_dict = {
#             'GMST': None,
#             'GMRESTOM': None,
#             'GMLWCF': None,
#             'GMSWCF': None,
#         }
#         for k, v in self.case_dict.items():
#             if 'fig' not in locals():
#                 fig, ax = v.plot_ts(color_dict=_clr_dict, label=v.name, **plot_kws)
#             else:
#                 ax = v.plot_ts(ax=ax, color_dict=_clr_dict, label=v.name, **plot_kws)

#         _lgd_kws = {
#             'frameon': False,
#             'loc': 'upper left',
#             'bbox_to_anchor': [1.1, 1],
#         }
#         if lgd_kws is not None:
#             _lgd_kws.update(lgd_kws)

#         vn = list(ax.keys())[lgd_idx]
#         ax[vn].legend(**_lgd_kws)

#         return fig, ax