import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class GraficoCluster:
    def __init__(self, datos):
        self.datos = datos
        self.colores = None
        self.titulo = "Distribucion variable"
        self.figsize = (12,4)

    def configurar_colores(self, colores):
        self.colores = colores

    def configurar_titulo(self, titulo):
        self.titulo = titulo

    def configurar_figsize(self, figsize):
        self.figsize = figsize

    # Falta: figsize (hay que predefinir), y_label, x_label

    def mostrar(self):
        pass

class GraficoHistograma(GraficoCluster):
    def mostrar(self, col, bins=10, log=False, histtype="bar"):
      fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=self.figsize)
      # El color va dentro del hist
      ax.hist(self.datos[col], bins=bins, range=(0, self.datos[col].max()), log=log, histtype=histtype, color = self.colores)
      # El titulo va dento de set_title
      ax.set_title(self.titulo); ax.set_xlabel(col); ax.set_ylabel("Recuento")
      fig.show()

class GraficoDeBarras(GraficoCluster):
    def mostrar(self, col, order_df=None):
      datosg = self.datos.groupby(by=col).size().reset_index().rename(columns={0:"Recuento"})
      if isinstance(order_df, pd.DataFrame):
        datosg = datosg.merge(order_df, on=col, how="left").sort_values(by="order")
      x_coor = np.arange(datosg.shape[0])
      height = datosg["Recuento"]
      x_labels = datosg[col]

      fig, ax = plt.subplots(1, 1, constrained_layout=True, figsize=self.figsize)
      # El color va dentro del bar
      ax.bar(x_coor, height, color = self.colores)
      # El titulo va dentro de set title
      ax.set_title(self.titulo); ax.set_xlabel(col); ax.set_ylabel("Recuento")
      ax.set_xticks(x_coor, x_labels, rotation=20, horizontalalignment="right")
      fig.show()

class GraficoHistogramaCluster(GraficoCluster):
    def mostrar(self, col, bins=20, log=False, histtype="step"):
      datos = self.datos
      cluster_values = datos["cluster"].unique()
      n_clusters = datos["cluster"].nunique()
      min_ = datos[col].min(); max_ = datos[col].max()

      plot_nrows = n_clusters // 3 + min(1, n_clusters % 3)
      print(plot_nrows)
      fig, ax = plt.subplots(plot_nrows, 3, constrained_layout=True, figsize=self.figsize)
      for n in range(n_clusters):
        plot_row = n // 3; plot_col = n % 3
        # Dentro del hist van los colores
        ax[plot_row, plot_col].hist(datos.loc[datos["cluster"] == n, col], bins=bins, range=(min_, max_), log=log, histtype=histtype, density=True, color = self.colores)
        # Dentro del set title va el titulo
        ax[plot_row, plot_col].set_title(self.titulo); ax[plot_row, plot_col].set_xlabel(col); ax[plot_row, plot_col].set_ylabel("Density")
      fig.show()

class GraficoDeBarrasCluster(GraficoCluster):
    def mostrar(self, col, order_df=None):
      datosg = self.datos.groupby(by=[col, "cluster"]).size().reset_index().rename(columns={0:"Recuento"})
      cluster_values = datosg["cluster"].unique()
      n_clusters = datosg["cluster"].nunique()
      group_values = datosg[col].unique()
      for group_value in group_values:
        n_clusters_group = datosg.loc[datosg[col] == group_value, "cluster"].nunique()
        cluster_values_group = datosg.loc[datosg[col] == group_value, "cluster"].unique()
        if n_clusters != n_clusters_group:
          cluster_values_missing = [x for x in cluster_values if x not in cluster_values_group]
          # datosg = datosg.concat(
          #     pd.DataFrame({
          #         col:[group_value] * len(cluster_values_missing),
          #         'cluster':cluster_values_missing,
          #         'Recuento':[0] * len(cluster_values_missing)}),
          #     ignore_index=True,
          #     axis=0
          #     )
          datos_to_concat = pd.DataFrame({
                  col:[group_value] * len(cluster_values_missing),
                  'cluster':cluster_values_missing,
                  'Recuento':[0] * len(cluster_values_missing)
                  })
          datosg = pd.concat([datosg, datos_to_concat], ignore_index=True, axis=0)

      if isinstance(order_df, pd.DataFrame):
        datosg = datosg.merge(order_df, on=col, how="left").sort_values(by="order")

      bar_width = 0.8
      n_groups = datosg[col].nunique()
      n_clusters = datosg["cluster"].nunique()
      bar_ind_width = bar_width / n_clusters
      x_coor_base = np.arange(n_groups)
      x_labels = datosg[col].unique()
      offset = bar_ind_width / 2
      groups_max = datosg.loc[:, [col, "Recuento"]].groupby(by=col).sum().reset_index().rename(columns={"Recuento":"total"})
      datosg = datosg.merge(groups_max, on=col, how="left")
      datosg["Porcentaje"] = datosg["Recuento"].div(datosg["total"])

      fig, ax = plt.subplots(1, 2, constrained_layout=True, figsize=self.figsize)
      for n in cluster_values:
      # for n in range(n_clusters):
        x_coor = x_coor_base + offset - bar_width / 2
        height = datosg.loc[datosg["cluster"] == n, "Recuento"].values
        height_per = datosg.loc[datosg["cluster"] == n, "Porcentaje"].values
        # Dento del bar van los colores
        ax[0].bar(x_coor, height, width=bar_ind_width, label="cluster " + str(n), color = self.colores)
        ax[1].bar(x_coor, height_per, width=bar_ind_width, label="cluster " + str(n), color = self.colores)
        offset += bar_ind_width
      ax[0].set_title(self.titulo); ax[0].set_xlabel(col); ax[0].set_ylabel("Recuento"); ax[0].legend(loc='upper center')
      ax[0].set_xticks(x_coor_base, x_labels, rotation=20, horizontalalignment="right")
      # Dentro del titulo va el titulo
      ax[1].set_title(self.titulo); ax[1].set_xlabel(col); ax[1].set_ylabel("Porcentaje"); ax[1].legend(loc='upper center', ncols=2)
      ax[1].set_xticks(x_coor_base, x_labels, rotation=20, horizontalalignment="right")
      fig.show()