"""
Data schema for traffic sign holder detection and analysis.
Defines structured output format suitable for database storage and model training.
"""

from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

# Enums for classification attributes
MaterialType = Literal[
    "metal", "concrete", "wood", "plastic", "building/wall", "other"
]

OwnerType = Literal[
    "city", "municipality", "other"
]

BaseType = Literal[
    "single pole", "double pole", "triple pole", "quadruple pole",
    "streetlight pole", "power line pole", "telecom pole", "traffic light pole",
    "traffic equipment", "portal construction", "bridge construction",
    "guardrail/railing", "bus stop shelter", "fence", "building",
    "gate/door", "barrier", "street name plate pole", "directional plate pole",
    "guiding board Klemmfix", "temporary sign stand", "Z4 guiding device", "other"
]

OrientationType = Literal[
    "in driving direction", "perpendicular to driving direction", 
    "against driving direction", "other"
]


class BoundingBox(BaseModel):
    """Bounding box coordinates in pixel space."""
    x_min: int = Field(..., description="Left edge pixel coordinate")
    y_min: int = Field(..., description="Top edge pixel coordinate") 
    x_max: int = Field(..., description="Right edge pixel coordinate")
    y_max: int = Field(..., description="Bottom edge pixel coordinate")
    width: int = Field(..., description="Bounding box width in pixels")
    height: int = Field(..., description="Bounding box height in pixels")
    
    def __init__(self, **data):
        super().__init__(**data)
        # Auto-calculate width and height if not provided
        if 'width' not in data:
            self.width = self.x_max - self.x_min
        if 'height' not in data:
            self.height = self.y_max - self.y_min


class ConfidenceScores(BaseModel):
    """Confidence scores for various predictions."""
    detection: float = Field(..., ge=0.0, le=1.0, description="Holder detection confidence")
    material: float = Field(..., ge=0.0, le=1.0, description="Material classification confidence")
    owner: float = Field(..., ge=0.0, le=1.0, description="Owner classification confidence") 
    base_type: float = Field(..., ge=0.0, le=1.0, description="Base type classification confidence")
    orientation: float = Field(..., ge=0.0, le=1.0, description="Orientation classification confidence")


class TrafficSignPlate(BaseModel):
    """Individual traffic sign plate mounted on a holder."""
    plate_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique plate identifier")
    bounding_box: BoundingBox = Field(..., description="Sign plate bounding box")
    ocr_text: str = Field(..., description="Extracted text, numbers, or arrows (use 'no text' if none)")
    ocr_confidence: float = Field(..., ge=0.0, le=1.0, description="OCR extraction confidence")
    notes: Optional[str] = Field(None, description="Additional notes about the sign plate")


class TrafficSignHolder(BaseModel):
    """Main holder object with all attributes and mounted signs."""
    holder_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique holder identifier")
    bounding_box: BoundingBox = Field(..., description="Holder bounding box with green marking")
    
    # Classification attributes
    material: MaterialType = Field(..., description="Holder material type")
    owner: OwnerType = Field(..., description="Holder owner type")
    base_type: BaseType = Field(..., description="Holder base/structure type")
    orientation: OrientationType = Field(..., description="Holder orientation relative to driving direction")
    
    # Confidence scores
    confidence: ConfidenceScores = Field(..., description="Confidence scores for all predictions")
    
    # Mounted traffic sign plates
    traffic_signs: List[TrafficSignPlate] = Field(default_factory=list, description="List of traffic sign plates on this holder")
    
    # Additional information
    notes: Optional[str] = Field(None, description="Notes about uncertainties, occlusions, or multiple interpretations")
    custom_attributes: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional custom attributes")


class ImageMetadata(BaseModel):
    """Metadata about the analyzed image."""
    filename: str = Field(..., description="Image filename")
    file_path: str = Field(..., description="Full path to image file")
    image_width: int = Field(..., description="Image width in pixels")
    image_height: int = Field(..., description="Image height in pixels")
    file_size_bytes: int = Field(..., description="Image file size in bytes")
    creation_date: Optional[datetime] = Field(None, description="Image creation timestamp")
    
    # GPS/Location data (if available)
    latitude: Optional[float] = Field(None, description="GPS latitude")
    longitude: Optional[float] = Field(None, description="GPS longitude")
    altitude: Optional[float] = Field(None, description="GPS altitude")
    bearing: Optional[float] = Field(None, description="Camera bearing/direction")


class AnalysisMetadata(BaseModel):
    """Metadata about the analysis process."""
    analysis_id: str = Field(default_factory=lambda: str(uuid.uuid4()), description="Unique analysis identifier")
    timestamp: datetime = Field(default_factory=datetime.now, description="Analysis timestamp")
    model_version: str = Field(..., description="Version of the detection model used")
    processing_time_seconds: float = Field(..., description="Total processing time")
    
    # Model configuration
    detection_threshold: float = Field(0.5, description="Detection confidence threshold used")
    nms_threshold: float = Field(0.4, description="Non-maximum suppression threshold")
    
    # Analysis statistics
    total_holders_detected: int = Field(0, description="Total number of holders detected")
    total_signs_detected: int = Field(0, description="Total number of sign plates detected")


class TrafficSignAnalysis(BaseModel):
    """Complete analysis result for one image."""
    analysis_metadata: AnalysisMetadata = Field(..., description="Analysis process metadata")
    image_metadata: ImageMetadata = Field(..., description="Source image metadata")
    holders: List[TrafficSignHolder] = Field(default_factory=list, description="List of detected holders")
    
    # Global analysis notes
    global_notes: Optional[str] = Field(None, description="Overall analysis notes or issues")
    
    # Quality metrics
    image_quality_score: Optional[float] = Field(None, ge=0.0, le=1.0, description="Overall image quality score")
    lighting_condition: Optional[str] = Field(None, description="Lighting conditions (good/poor/mixed)")
    weather_condition: Optional[str] = Field(None, description="Weather conditions if visible")

    def get_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics for the analysis."""
        total_signs = sum(len(holder.traffic_signs) for holder in self.holders)
        
        # Material distribution
        materials = [holder.material for holder in self.holders]
        material_counts = {mat: materials.count(mat) for mat in set(materials)}
        
        # Base type distribution  
        base_types = [holder.base_type for holder in self.holders]
        base_type_counts = {bt: base_types.count(bt) for bt in set(base_types)}
        
        return {
            "total_holders": len(self.holders),
            "total_signs": total_signs,
            "material_distribution": material_counts,
            "base_type_distribution": base_type_counts,
            "average_detection_confidence": sum(h.confidence.detection for h in self.holders) / max(len(self.holders), 1),
            "processing_time": self.analysis_metadata.processing_time_seconds
        }


# Database table schemas for SQLAlchemy (optional)
class DatabaseSchema:
    """SQL schema definitions for database storage."""
    
    @staticmethod
    def get_create_statements() -> List[str]:
        """Return SQL CREATE statements for all tables."""
        return [
            """
            CREATE TABLE IF NOT EXISTS analyses (
                analysis_id TEXT PRIMARY KEY,
                timestamp DATETIME,
                filename TEXT,
                file_path TEXT,
                image_width INTEGER,
                image_height INTEGER,
                model_version TEXT,
                processing_time_seconds REAL,
                total_holders_detected INTEGER,
                total_signs_detected INTEGER,
                global_notes TEXT,
                image_quality_score REAL,
                latitude REAL,
                longitude REAL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS holders (
                holder_id TEXT PRIMARY KEY,
                analysis_id TEXT,
                x_min INTEGER,
                y_min INTEGER, 
                x_max INTEGER,
                y_max INTEGER,
                material TEXT,
                owner TEXT,
                base_type TEXT,
                orientation TEXT,
                detection_confidence REAL,
                material_confidence REAL,
                owner_confidence REAL,
                base_type_confidence REAL,
                orientation_confidence REAL,
                notes TEXT,
                FOREIGN KEY (analysis_id) REFERENCES analyses (analysis_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS traffic_signs (
                plate_id TEXT PRIMARY KEY,
                holder_id TEXT,
                x_min INTEGER,
                y_min INTEGER,
                x_max INTEGER, 
                y_max INTEGER,
                ocr_text TEXT,
                ocr_confidence REAL,
                notes TEXT,
                FOREIGN KEY (holder_id) REFERENCES holders (holder_id)
            )
            """
        ]


# Export formats for training data
class COCOFormat(BaseModel):
    """COCO format export for object detection training."""
    pass

class YOLOFormat(BaseModel):
    """YOLO format export for object detection training.""" 
    pass