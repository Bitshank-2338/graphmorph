from fastapi import APIRouter, UploadFile, File

from app.utils.csv_parser import parse_csv
from app.utils.graph_transformer import transform_to_graph
from app.services.graph_builder import build_graph
from app.services.ui_generator import generate_default_ui

router = APIRouter()


@router.post("/upload")
async def upload_dataset(file: UploadFile = File(...)):
    df = parse_csv(file)
    graph_data = transform_to_graph(df)
    write_stats = build_graph(graph_data)
    ui_schema = generate_default_ui(graph_data)

    return {
        "message": "Dataset uploaded and transformed.",
        "stats": graph_data["stats"],
        "writes": write_stats,
        "reasoning": [
            f"Parsed {len(df)} rows · {len(df.columns)} cols",
            f"Detected entity types: {', '.join(graph_data['stats']['entity_types']) or 'none'}",
            f"Built graph: {graph_data['stats']['node_count']} nodes, "
            f"{graph_data['stats']['edge_count']} edges",
            "Initial relationship explorer ready.",
        ],
        "ui_schema": ui_schema,
    }
