def get_versions():
    return versions[0]["number"]


versions = [
    {
        "number": "0.0.40",
        "features": [
            "1. add SyntenyLinkPlotJob in synteny_block",
            "2. debug",
        ],
    },
    {
        "number": "0.0.39",
        "features": [
            "1. debug",
            "2. update synteny_block",
        ],
    },
    {
        "number": "0.0.38",
        "features": [
            "1. Use /run/user as tmp file",
            "2. add plot_data_histogram_in_screen in histogram",
            "3. Separating code from ToolBiox",
            "4. debug",
        ],
    },
    {
        "number": "0.0.37",
        "features": [
            "1. add confidence_threshold for orthologous extraction from gene tree",
        ],
    },
    {
        "number": "0.0.36",
        "features": [
            "1. Add miniprot parser",
        ],
    },
    {
        "number": "0.0.35",
        "features": [
            "1. change in synteny block",
        ],
    },
    {
        "number": "0.0.34",
        "features": [
            "1. change in synteny block",
        ],
    },
    {
        "number": "0.0.33",
        "features": [
            "1. change in synteny block",
        ],
    },
    {
        "number": "0.0.32",
        "features": [
            "1. change in synteny block",
        ],
    },
    {
        "number": "0.0.31",
        "features": [
            "1. change in synteny block",
        ],
    },
    {
        "number": "0.0.30",
        "features": [
            "1. limit biopython to 1.80",
        ],
    },
    {
        "number": "0.0.29",
        "features": [
            "1. add ancestral karyotype function",
        ],
    },
    {
        "number": "0.0.28",
        "features": [
            "1. Separate code about RNA-seq from ToolBiox",
        ],
    },
    {
        "number": "0.0.27",
        "features": [
            "1. synteny_block update",
        ],
    },
    {
        "number": "0.0.26",
        "features": [
            "1. erase the trying of improve multiprocess_running",
            "2. add wgdi_collinearity in new synteny_block model",
        ],
    },
    {
        "number": "0.0.25",
        "features": [
            "1. try to improve multiprocess_running, but failed",
        ],
    },
    {
        "number": "0.0.24",
        "features": [
            "1. modify map_node_species_info in tree_operate",
        ],
    },
    {
        "number": "0.0.23",
        "features": [
            "1. modify map_node_species_info in tree_operate",
        ],
    },
    {
        "number": "0.0.22",
        "features": [
            "1. debug",
        ],
    },
    {
        "number": "0.0.21",
        "features": [
            "1. debug",
        ],
    },
    {
        "number": "0.0.20",
        "features": [
            "1. add iqtree in phylogenomics.py",
        ],
    },
    {
        "number": "0.0.19",
        "features": [
            "1. add stick plot in toolbiox.api.xuyuxing.plot.base",
            "2. add make_unique_name in tree_operate",
        ],
    },
    {
        "number": "0.0.18",
        "features": [
            "1. update for add_contig_grid",
        ],
    },
    {
        "number": "0.0.17",
        "features": [
            "1. add optimize",
        ],
    },
    {
        "number": "0.0.16",
        "features": [
            "1. debug",
        ],
    },
    {
        "number": "0.0.15",
        "features": [
            "1. modify genome_feature2",
        ],
    },
    {
        "number": "0.0.14",
        "features": [
            "1. add get_file_md5",
            "2. debug",
        ],
    },
    {
        "number": "0.0.13",
        "features": [
            "1. rewrite store_dict_to_db in sqlite_command",
            "2. debug",
        ],
    },
    {
        "number": "0.0.12",
        "features": [
            "1. debug",
        ],
    },
    {
        "number": "0.0.11",
        "features": [
            "1. debug",
        ],
    },
    {
        "number": "0.0.10",
        "features": [
            "1. Separate WPGmapper from ToolBiox",
            "2. Add pickle function in sqlite",
        ],
    },
    {
        "number": "0.0.9",
        "features": [
            "1. debug",
        ],
    },
    {
        "number": "0.0.8",
        "features": [
            "1. Add ftp function",
            "2. Simplifies the process of loading gff into sqlite",
        ],
    },
    {
        "number": "0.0.7",
        "features": [
            "1. Separate SeqParser from ToolBiox",
        ],
    },
    {
        "number": "0.0.6",
        "features": [
            "1. bug fixed",
        ],
    },
    {
        "number": "0.0.5",
        "features": [
            "1. bug fixed",
        ],
    },
    {
        "number": "0.0.4",
        "features": [
            "1. Separate TaxonTools from ToolBiox",
            "2. Add some package in setup.py",
        ],
    },
    {
        "number": "0.0.3",
        "features": [
            "1. Organized all import code",
            "2. Add function for get common tree by 1kp",
        ],
    },
    {
        "number": "0.0.2.1",
        "features": [
            "1. Get rid of the dependency on scikit-bio",
            "2. Reformat TaxonTools.py",
        ],
    },
    {
        "number": "0.0.2",
        "features": [
            "1. Get rid of the dependency on scikit-bio",
        ],
    },
    {
        "number": "0.0.1",
        "features": [
            "1. Separate the tools, libraries and api parts from the original Genome_work_tools and become ToolBiox",
        ],
    },
]