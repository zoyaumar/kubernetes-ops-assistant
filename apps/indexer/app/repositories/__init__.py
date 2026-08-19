"""
Database repository layer.

Repositories abstract all SQL away from the processing pipeline.
Each repository takes an asyncpg connection or SQLAlchemy AsyncSession.
"""
