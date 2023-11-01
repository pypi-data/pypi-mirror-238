import torch
from opengsl.module.functional import normalize
from opengsl.module.encoder import GCNDiagEncoder, GCNEncoder, APPNPEncoder, GINEncoder, MLPEncoder
from opengsl.module.fuse import Interpolate
from opengsl.module.transform import Normalize, KNN, Symmetry
from opengsl.module.metric import InnerProduct, WeightedCosine, GeneralizedMetric
from opengsl.module.graphlearner import GraphLearner


class GGSL(torch.nn.Module):

    def __init__(self, num_nodes, num_features, num_classes, device, conf):
        super(GGSL, self).__init__()

        # gsl encoder
        d_metric = conf.gsl['n_hidden_2']
        if conf.gsl['model_type'] == 'diag':
            self.encoder = GCNDiagEncoder(2, num_features)
            d_metric = num_features
        elif conf.gsl['model_type'] == 'gcn':
            self.encoder = GCNEncoder(num_features, conf.gsl['n_hidden_1'], conf.gsl['n_hidden_2'], conf.gsl['n_layers'],
                                      conf.gsl['dropout'])
        elif conf.gsl['model_type'] == 'appnp':
            self.encoder = APPNPEncoder(num_features, conf.gsl['n_hidden_1'], conf.gsl['n_hidden_2'],
                                        dropout=conf.gsl['dropout'], K=conf.gsl['K_APPNP'], alpha=conf.gsl['alpha'],
                                        spmm_type=1)
        elif conf.gsl['model_type'] == 'gin':
            self.encoder = GINEncoder(num_features, conf.gsl['n_hidden_1'], conf.gsl['n_hidden_2'],
                                        conf.gsl['n_layers'], conf.gsl['mlp_layers'], spmm_type=1)
        elif conf.gsl['model_type'] == 'mlp':
            self.encoder = MLPEncoder(num_features, conf.gsl['n_hidden_1'], conf.gsl['n_hidden_2'],
                                        conf.gsl['n_layers'], dropout=conf.gsl['dropout'])
        # self.metric = WeightedCosine(d_metric, 1, False, conf.gsl['normalize'])
        self.metric = GeneralizedMetric(d_metric, 2, conf.gsl['normalize'])

        self.normalize_a = Normalize(add_loop=False)
        self.normalize_e = Normalize('row-norm', p=2)
        self.knn = KNN(conf.gsl['K'], sparse_out=True)
        self.sym = Symmetry(1)
        self.fuse = Interpolate(1, 1)
        self.graphlearner = GraphLearner(encoder=self.encoder, metric=self.metric, postprocess=[self.knn, self.sym], fuse=self.fuse)

        # task encoder
        if conf.model['type'] == 'gcn':
            self.conv_task = GCNEncoder(num_features, conf.model['n_hidden'], num_classes, conf.model['n_layers'],
                                 conf.model['dropout'], conf.model['input_dropout'], conf.model['norm'],
                                 conf.model['n_linear'], conf.model['spmm_type'], conf.model['act'],
                                 conf.model['input_layer'], conf.model['output_layer'])
        elif conf.model['type'] == 'appnp':
            self.conv_task = APPNPEncoder(num_features, conf.model['n_hidden'], num_classes,
                               dropout=conf.model['dropout'], K=conf.model['K_APPNP'],
                               alpha=conf.model['alpha'], spmm_type=1)
        elif conf.model['type'] == 'gin':
            self.conv_task = GINEncoder(num_features, conf.model['n_hidden'], num_classes,
                               conf.model['n_layers'], conf.model['mlp_layers'], spmm_type=1)






    def graph_parameters(self):
        return list(self.graphlearner.parameters())

    def base_parameters(self):
        return list(self.conv_task.parameters())

    def forward(self, input, Adj):
        adjs = {}
        Adj.requires_grad = False
        norm_Adj = self.normalize_a(Adj)

        # gsl encoder
        node_embeddings = self.encoder(input, norm_Adj)
        # metric
        Adj_new = self.metric(node_embeddings)
        # postprocess
        Adj_new = self.knn(adj=Adj_new)
        Adj_new = self.sym(Adj_new)
        # fuse
        Adj_final = self.fuse(Adj_new, Adj)

        # task
        Adj_final_norm = self.normalize_a(Adj_final.coalesce())
        x = self.conv_task(input, Adj_final_norm)

        adjs['new'] = Adj_new
        adjs['final'] = Adj_final

        return x, adjs, node_embeddings
