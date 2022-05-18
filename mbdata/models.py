# Automatically generated, do not edit

# pylint: disable=C0103
# pylint: disable=C0302
# pylint: disable=W0232

from sqlalchemy import Column, Index, Integer, String, Text, ForeignKey, Boolean, DateTime, Time, Date, Enum, Interval, CHAR, CheckConstraint, sql
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, composite, backref
from mbdata.types import PartialDate, Point, Cube as _Cube, regexp, UUID, SMALLINT, BIGINT, JSONB
from typing import Any, Union

import mbdata.config
mbdata.config.freeze()

Base = None  # type: Any

if mbdata.config.Base is not None:
    Base = mbdata.config.Base
elif mbdata.config.metadata is not None:
    Base = declarative_base(metadata=mbdata.config.metadata)
else:
    Base = declarative_base()

if mbdata.config.use_cube:
    Cube = _Cube  # type: Union[_Cube, Text]
else:
    Cube = Text


def apply_schema(name, schema):
    schema = mbdata.config.schemas.get(schema, schema)
    if schema:
        name = "{}.{}".format(schema, name)
    return name


class AlternativeRelease(Base):
    __tablename__ = 'alternative_release'
    __table_args__ = (
        Index('alternative_release_idx_name', 'name'),
        Index('alternative_release_idx_artist_credit', 'artist_credit'),
        Index('alternative_release_idx_language_script', 'language', 'script'),
        Index('alternative_release_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='alternative_release_fk_release'), nullable=False)
    name = Column(String)
    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='alternative_release_fk_artist_credit'))
    type_id = Column('type', Integer, ForeignKey(apply_schema('alternative_release_type.id', 'musicbrainz'), name='alternative_release_fk_type'), nullable=False)
    language_id = Column('language', Integer, ForeignKey(apply_schema('language.id', 'musicbrainz'), name='alternative_release_fk_language'), nullable=False)
    script_id = Column('script', Integer, ForeignKey(apply_schema('script.id', 'musicbrainz'), name='alternative_release_fk_script'), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))

    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)
    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id])
    type = relationship('AlternativeReleaseType', foreign_keys=[type_id], innerjoin=True)
    language = relationship('Language', foreign_keys=[language_id], innerjoin=True)
    script = relationship('Script', foreign_keys=[script_id], innerjoin=True)


class AlternativeReleaseType(Base):
    __tablename__ = 'alternative_release_type'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('alternative_release_type.id', 'musicbrainz'), name='alternative_release_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('AlternativeReleaseType', foreign_keys=[parent_id])


class AlternativeMedium(Base):
    __tablename__ = 'alternative_medium'
    __table_args__ = (
        Index('alternative_medium_idx_alternative_release', 'alternative_release'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    medium_id = Column('medium', Integer, ForeignKey(apply_schema('medium.id', 'musicbrainz'), name='alternative_medium_fk_medium'), nullable=False)
    alternative_release_id = Column('alternative_release', Integer, ForeignKey(apply_schema('alternative_release.id', 'musicbrainz'), name='alternative_medium_fk_alternative_release'), nullable=False)
    name = Column(String)

    medium = relationship('Medium', foreign_keys=[medium_id], innerjoin=True)
    alternative_release = relationship('AlternativeRelease', foreign_keys=[alternative_release_id], innerjoin=True)


class AlternativeTrack(Base):
    __tablename__ = 'alternative_track'
    __table_args__ = (
        Index('alternative_track_idx_name', 'name'),
        Index('alternative_track_idx_artist_credit', 'artist_credit'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String)
    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='alternative_track_fk_artist_credit'))
    ref_count = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))

    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id])


class AlternativeMediumTrack(Base):
    __tablename__ = 'alternative_medium_track'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    alternative_medium_id = Column('alternative_medium', Integer, ForeignKey(apply_schema('alternative_medium.id', 'musicbrainz'), name='alternative_medium_track_fk_alternative_medium'), nullable=False, primary_key=True)
    track_id = Column('track', Integer, ForeignKey(apply_schema('track.id', 'musicbrainz'), name='alternative_medium_track_fk_track'), nullable=False, primary_key=True)
    alternative_track_id = Column('alternative_track', Integer, ForeignKey(apply_schema('alternative_track.id', 'musicbrainz'), name='alternative_medium_track_fk_alternative_track'), nullable=False)

    alternative_medium = relationship('AlternativeMedium', foreign_keys=[alternative_medium_id], innerjoin=True)
    track = relationship('Track', foreign_keys=[track_id], innerjoin=True)
    alternative_track = relationship('AlternativeTrack', foreign_keys=[alternative_track_id], innerjoin=True)


class Annotation(Base):
    __tablename__ = 'annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='annotation_fk_editor'), nullable=False)
    text = Column(String)
    changelog = Column(String(255))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class Application(Base):
    __tablename__ = 'application'
    __table_args__ = (
        Index('application_idx_owner', 'owner'),
        Index('application_idx_oauth_id', 'oauth_id', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    owner_id = Column('owner', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='application_fk_owner'), nullable=False)
    name = Column(String, nullable=False)
    oauth_id = Column(String, nullable=False)
    oauth_secret = Column(String, nullable=False)
    oauth_redirect_uri = Column(String)

    owner = relationship('Editor', foreign_keys=[owner_id], innerjoin=True)


class AreaType(Base):
    __tablename__ = 'area_type'
    __table_args__ = (
        Index('area_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area_type.id', 'musicbrainz'), name='area_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('AreaType', foreign_keys=[parent_id])


class Area(Base):
    __tablename__ = 'area'
    __table_args__ = (
        Index('area_idx_gid', 'gid', unique=True),
        Index('area_idx_name', 'name'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    type_id = Column('type', Integer, ForeignKey(apply_schema('area_type.id', 'musicbrainz'), name='area_fk_type'))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))

    type = relationship('AreaType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class AreaGIDRedirect(Base):
    __tablename__ = 'area_gid_redirect'
    __table_args__ = (
        Index('area_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Area', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def area(self):
        return self.redirect


class AreaAliasType(Base):
    __tablename__ = 'area_alias_type'
    __table_args__ = (
        Index('area_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area_alias_type.id', 'musicbrainz'), name='area_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('AreaAliasType', foreign_keys=[parent_id])


class AreaAlias(Base):
    __tablename__ = 'area_alias'
    __table_args__ = (
        Index('area_alias_idx_area', 'area'),
        Index('area_alias_idx_primary', 'area', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_alias_fk_area'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('area_alias_type.id', 'musicbrainz'), name='area_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    type = relationship('AreaAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class AreaAnnotation(Base):
    __tablename__ = 'area_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_annotation_fk_area'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='area_annotation_fk_annotation'), nullable=False, primary_key=True)

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class AreaAttributeType(Base):
    __tablename__ = 'area_attribute_type'
    __table_args__ = (
        Index('area_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area_attribute_type.id', 'musicbrainz'), name='area_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('AreaAttributeType', foreign_keys=[parent_id])


class AreaAttributeTypeAllowedValue(Base):
    __tablename__ = 'area_attribute_type_allowed_value'
    __table_args__ = (
        Index('area_attribute_type_allowed_value_idx_name', 'area_attribute_type'),
        Index('area_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    area_attribute_type_id = Column('area_attribute_type', Integer, ForeignKey(apply_schema('area_attribute_type.id', 'musicbrainz'), name='area_attribute_type_allowed_value_fk_area_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area_attribute_type_allowed_value.id', 'musicbrainz'), name='area_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    area_attribute_type = relationship('AreaAttributeType', foreign_keys=[area_attribute_type_id], innerjoin=True)
    parent = relationship('AreaAttributeTypeAllowedValue', foreign_keys=[parent_id])


class AreaAttribute(Base):
    __tablename__ = 'area_attribute'
    __table_args__ = (
        Index('area_attribute_idx_area', 'area'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_attribute_fk_area'), nullable=False)
    area_attribute_type_id = Column('area_attribute_type', Integer, ForeignKey(apply_schema('area_attribute_type.id', 'musicbrainz'), name='area_attribute_fk_area_attribute_type'), nullable=False)
    area_attribute_type_allowed_value_id = Column('area_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('area_attribute_type_allowed_value.id', 'musicbrainz'), name='area_attribute_fk_area_attribute_type_allowed_value'))
    area_attribute_text = Column(String)

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    area_attribute_type = relationship('AreaAttributeType', foreign_keys=[area_attribute_type_id], innerjoin=True)
    area_attribute_type_allowed_value = relationship('AreaAttributeTypeAllowedValue', foreign_keys=[area_attribute_type_allowed_value_id])


class AreaContainment(Base):
    __tablename__ = 'area_containment'
    __table_args__ = (
        Index('area_containment_idx_parent', 'parent'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    descendant_id = Column('descendant', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_containment_fk_descendant'), nullable=False, primary_key=True)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_containment_fk_parent'), nullable=False, primary_key=True)
    depth = Column(SMALLINT, nullable=False)

    descendant = relationship('Area', foreign_keys=[descendant_id], innerjoin=True)
    parent = relationship('Area', foreign_keys=[parent_id], innerjoin=True)


class AreaTag(Base):
    __tablename__ = 'area_tag'
    __table_args__ = (
        Index('area_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_tag_fk_area'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='area_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class AreaTagRaw(Base):
    __tablename__ = 'area_tag_raw'
    __table_args__ = (
        Index('area_tag_raw_idx_area', 'area'),
        Index('area_tag_raw_idx_tag', 'tag'),
        Index('area_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='area_tag_raw_fk_area'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='area_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='area_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class Artist(Base):
    __tablename__ = 'artist'
    __table_args__ = (
        Index('artist_idx_gid', 'gid', unique=True),
        Index('artist_idx_name', 'name'),
        Index('artist_idx_sort_name', 'sort_name'),
        Index('artist_idx_area', 'area'),
        Index('artist_idx_begin_area', 'begin_area'),
        Index('artist_idx_end_area', 'end_area'),
        Index('artist_idx_null_comment', 'name', unique=True),
        Index('artist_idx_uniq_name_comment', 'name', 'comment', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    gid = Column(UUID, nullable=False)
    name = Column(String, nullable=False)
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    type_id = Column('type', Integer, ForeignKey(apply_schema('artist_type.id', 'musicbrainz'), name='artist_fk_type'))
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='artist_fk_area'))
    gender_id = Column('gender', Integer, ForeignKey(apply_schema('gender.id', 'musicbrainz'), name='artist_fk_gender'))
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    begin_area_id = Column('begin_area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='artist_fk_begin_area'))
    end_area_id = Column('end_area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='artist_fk_end_area'))

    type = relationship('ArtistType', foreign_keys=[type_id])
    area = relationship('Area', foreign_keys=[area_id])
    gender = relationship('Gender', foreign_keys=[gender_id])
    begin_area = relationship('Area', foreign_keys=[begin_area_id])
    end_area = relationship('Area', foreign_keys=[end_area_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class ArtistAliasType(Base):
    __tablename__ = 'artist_alias_type'
    __table_args__ = (
        Index('artist_alias_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('artist_alias_type.id', 'musicbrainz'), name='artist_alias_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ArtistAliasType', foreign_keys=[parent_id])


class ArtistAlias(Base):
    __tablename__ = 'artist_alias'
    __table_args__ = (
        Index('artist_alias_idx_artist', 'artist'),
        Index('artist_alias_idx_primary', 'artist', 'locale', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_alias_fk_artist'), nullable=False)
    name = Column(String, nullable=False)
    locale = Column(String)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    type_id = Column('type', Integer, ForeignKey(apply_schema('artist_alias_type.id', 'musicbrainz'), name='artist_alias_fk_type'))
    sort_name = Column(String, nullable=False)
    begin_date_year = Column(SMALLINT)
    begin_date_month = Column(SMALLINT)
    begin_date_day = Column(SMALLINT)
    end_date_year = Column(SMALLINT)
    end_date_month = Column(SMALLINT)
    end_date_day = Column(SMALLINT)
    primary_for_locale = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    ended = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    type = relationship('ArtistAliasType', foreign_keys=[type_id])

    begin_date = composite(PartialDate, begin_date_year, begin_date_month, begin_date_day)
    end_date = composite(PartialDate, end_date_year, end_date_month, end_date_day)


class ArtistAnnotation(Base):
    __tablename__ = 'artist_annotation'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_annotation_fk_artist'), nullable=False, primary_key=True)
    annotation_id = Column('annotation', Integer, ForeignKey(apply_schema('annotation.id', 'musicbrainz'), name='artist_annotation_fk_annotation'), nullable=False, primary_key=True)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    annotation = relationship('Annotation', foreign_keys=[annotation_id], innerjoin=True)


class ArtistAttributeType(Base):
    __tablename__ = 'artist_attribute_type'
    __table_args__ = (
        Index('artist_attribute_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    comment = Column(String(255), nullable=False, default='', server_default=sql.text("''"))
    free_text = Column(Boolean, nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('artist_attribute_type.id', 'musicbrainz'), name='artist_attribute_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ArtistAttributeType', foreign_keys=[parent_id])


class ArtistAttributeTypeAllowedValue(Base):
    __tablename__ = 'artist_attribute_type_allowed_value'
    __table_args__ = (
        Index('artist_attribute_type_allowed_value_idx_name', 'artist_attribute_type'),
        Index('artist_attribute_type_allowed_value_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    artist_attribute_type_id = Column('artist_attribute_type', Integer, ForeignKey(apply_schema('artist_attribute_type.id', 'musicbrainz'), name='artist_attribute_type_allowed_value_fk_artist_attribute_type'), nullable=False)
    value = Column(String)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('artist_attribute_type_allowed_value.id', 'musicbrainz'), name='artist_attribute_type_allowed_value_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    artist_attribute_type = relationship('ArtistAttributeType', foreign_keys=[artist_attribute_type_id], innerjoin=True)
    parent = relationship('ArtistAttributeTypeAllowedValue', foreign_keys=[parent_id])


class ArtistAttribute(Base):
    __tablename__ = 'artist_attribute'
    __table_args__ = (
        Index('artist_attribute_idx_artist', 'artist'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_attribute_fk_artist'), nullable=False)
    artist_attribute_type_id = Column('artist_attribute_type', Integer, ForeignKey(apply_schema('artist_attribute_type.id', 'musicbrainz'), name='artist_attribute_fk_artist_attribute_type'), nullable=False)
    artist_attribute_type_allowed_value_id = Column('artist_attribute_type_allowed_value', Integer, ForeignKey(apply_schema('artist_attribute_type_allowed_value.id', 'musicbrainz'), name='artist_attribute_fk_artist_attribute_type_allowed_value'))
    artist_attribute_text = Column(String)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    artist_attribute_type = relationship('ArtistAttributeType', foreign_keys=[artist_attribute_type_id], innerjoin=True)
    artist_attribute_type_allowed_value = relationship('ArtistAttributeTypeAllowedValue', foreign_keys=[artist_attribute_type_allowed_value_id])


class ArtistIPI(Base):
    __tablename__ = 'artist_ipi'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_ipi_fk_artist'), nullable=False, primary_key=True)
    ipi = Column(CHAR(11), nullable=False, primary_key=True)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True, backref=backref('ipis'))


class ArtistISNI(Base):
    __tablename__ = 'artist_isni'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_isni_fk_artist'), nullable=False, primary_key=True)
    isni = Column(CHAR(16), nullable=False, primary_key=True)
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True, backref=backref('isnis'))


class ArtistMeta(Base):
    __tablename__ = 'artist_meta'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column('id', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_meta_fk_id', ondelete='CASCADE'), nullable=False, primary_key=True)
    rating = Column(SMALLINT)
    rating_count = Column(Integer)

    artist = relationship('Artist', foreign_keys=[id], innerjoin=True, backref=backref('meta', uselist=False))


class ArtistTag(Base):
    __tablename__ = 'artist_tag'
    __table_args__ = (
        Index('artist_tag_idx_tag', 'tag'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_tag_fk_artist'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='artist_tag_fk_tag'), nullable=False, primary_key=True)
    count = Column(Integer, nullable=False)
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class ArtistRatingRaw(Base):
    __tablename__ = 'artist_rating_raw'
    __table_args__ = (
        Index('artist_rating_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_rating_raw_fk_artist'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='artist_rating_raw_fk_editor'), nullable=False, primary_key=True)
    rating = Column(SMALLINT, nullable=False)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)


class ArtistTagRaw(Base):
    __tablename__ = 'artist_tag_raw'
    __table_args__ = (
        Index('artist_tag_raw_idx_tag', 'tag'),
        Index('artist_tag_raw_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_tag_raw_fk_artist'), nullable=False, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='artist_tag_raw_fk_editor'), nullable=False, primary_key=True)
    tag_id = Column('tag', Integer, ForeignKey(apply_schema('tag.id', 'musicbrainz'), name='artist_tag_raw_fk_tag'), nullable=False, primary_key=True)
    is_upvote = Column(Boolean, nullable=False, default=True, server_default=sql.true())

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    tag = relationship('Tag', foreign_keys=[tag_id], innerjoin=True)


class ArtistCredit(Base):
    __tablename__ = 'artist_credit'
    __table_args__ = (
        Index('artist_credit_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    artist_count = Column(SMALLINT, nullable=False)
    ref_count = Column(Integer, default=0, server_default=sql.text('0'))
    created = Column(DateTime(timezone=True), server_default=sql.func.now())
    edits_pending = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    gid = Column(UUID, nullable=False)


class ArtistCreditGIDRedirect(Base):
    __tablename__ = 'artist_credit_gid_redirect'
    __table_args__ = (
        Index('artist_credit_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='artist_credit_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('ArtistCredit', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def artist_credit(self):
        return self.redirect


class ArtistCreditName(Base):
    __tablename__ = 'artist_credit_name'
    __table_args__ = (
        Index('artist_credit_name_idx_artist', 'artist'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    artist_credit_id = Column('artist_credit', Integer, ForeignKey(apply_schema('artist_credit.id', 'musicbrainz'), name='artist_credit_name_fk_artist_credit', ondelete='CASCADE'), nullable=False, primary_key=True)
    position = Column(SMALLINT, nullable=False, primary_key=True)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_credit_name_fk_artist', ondelete='CASCADE'), nullable=False)
    name = Column(String, nullable=False)
    join_phrase = Column(String, nullable=False, default='', server_default=sql.text("''"))

    artist_credit = relationship('ArtistCredit', foreign_keys=[artist_credit_id], innerjoin=True, backref=backref('artists', order_by="ArtistCreditName.position"))
    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)


class ArtistGIDRedirect(Base):
    __tablename__ = 'artist_gid_redirect'
    __table_args__ = (
        Index('artist_gid_redirect_idx_new_id', 'new_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    redirect_id = Column('new_id', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_gid_redirect_fk_new_id'), nullable=False)
    created = Column(DateTime(timezone=True), server_default=sql.func.now())

    redirect = relationship('Artist', foreign_keys=[redirect_id], innerjoin=True)

    @hybrid_property
    def new_id(self):
        return self.redirect_id

    @hybrid_property
    def artist(self):
        return self.redirect


class ArtistType(Base):
    __tablename__ = 'artist_type'
    __table_args__ = (
        Index('artist_type_idx_gid', 'gid', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    parent_id = Column('parent', Integer, ForeignKey(apply_schema('artist_type.id', 'musicbrainz'), name='artist_type_fk_parent'))
    child_order = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    description = Column(String)
    gid = Column(UUID, nullable=False)

    parent = relationship('ArtistType', foreign_keys=[parent_id])


class ArtistRelease(Base):
    __tablename__ = 'artist_release'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    is_track_artist = Column(Boolean, nullable=False)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_release_fk_artist'), nullable=False, primary_key=True)
    first_release_date = Column(Integer)
    catalog_numbers = Column(String)
    country_code = Column(CHAR(2))
    barcode = Column(BIGINT)
    sort_character = Column(CHAR(1), nullable=False)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='artist_release_fk_release'), nullable=False, primary_key=True)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)


class ArtistReleaseGroup(Base):
    __tablename__ = 'artist_release_group'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    is_track_artist = Column(Boolean, nullable=False)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='artist_release_group_fk_artist'), nullable=False, primary_key=True)
    unofficial = Column(Boolean, nullable=False)
    primary_type = Column(SMALLINT)
    secondary_types = Column(SMALLINT)
    first_release_date = Column(Integer)
    sort_character = Column(CHAR(1), nullable=False)
    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='artist_release_group_fk_release_group'), nullable=False, primary_key=True)

    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)
    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)


class AutoeditorElection(Base):
    __tablename__ = 'autoeditor_election'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    candidate_id = Column('candidate', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_fk_candidate'), nullable=False)
    proposer_id = Column('proposer', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_fk_proposer'), nullable=False)
    seconder_1_id = Column('seconder_1', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_fk_seconder_1'))
    seconder_2_id = Column('seconder_2', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_fk_seconder_2'))
    status = Column(Integer, nullable=False, default=1, server_default=sql.text('1'))
    yes_votes = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    no_votes = Column(Integer, nullable=False, default=0, server_default=sql.text('0'))
    propose_time = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())
    open_time = Column(DateTime(timezone=True))
    close_time = Column(DateTime(timezone=True))

    candidate = relationship('Editor', foreign_keys=[candidate_id], innerjoin=True)
    proposer = relationship('Editor', foreign_keys=[proposer_id], innerjoin=True)
    seconder_1 = relationship('Editor', foreign_keys=[seconder_1_id])
    seconder_2 = relationship('Editor', foreign_keys=[seconder_2_id])


class AutoeditorElectionVote(Base):
    __tablename__ = 'autoeditor_election_vote'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    autoeditor_election_id = Column('autoeditor_election', Integer, ForeignKey(apply_schema('autoeditor_election.id', 'musicbrainz'), name='autoeditor_election_vote_fk_autoeditor_election'), nullable=False)
    voter_id = Column('voter', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='autoeditor_election_vote_fk_voter'), nullable=False)
    vote = Column(Integer, nullable=False)
    vote_time = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())

    autoeditor_election = relationship('AutoeditorElection', foreign_keys=[autoeditor_election_id], innerjoin=True)
    voter = relationship('Editor', foreign_keys=[voter_id], innerjoin=True)


class CDTOC(Base):
    __tablename__ = 'cdtoc'
    __table_args__ = (
        Index('cdtoc_idx_discid', 'discid', unique=True),
        Index('cdtoc_idx_freedb_id', 'freedb_id'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    discid = Column(CHAR(28), nullable=False)
    freedb_id = Column(CHAR(8), nullable=False)
    track_count = Column(Integer, nullable=False)
    leadout_offset = Column(Integer, nullable=False)
    track_offset = Column(Integer, nullable=False)
    degraded = Column(Boolean, nullable=False, default=False, server_default=sql.false())
    created = Column(DateTime(timezone=True), server_default=sql.func.now())


class CDTOCRaw(Base):
    __tablename__ = 'cdtoc_raw'
    __table_args__ = (
        Index('cdtoc_raw_discid', 'discid'),
        Index('cdtoc_raw_toc', 'track_count', 'leadout_offset', 'track_offset', unique=True),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release_raw.id', 'musicbrainz'), name='cdtoc_raw_fk_release'), nullable=False)
    discid = Column(CHAR(28), nullable=False)
    track_count = Column(Integer, nullable=False)
    leadout_offset = Column(Integer, nullable=False)
    track_offset = Column(Integer, nullable=False)

    release = relationship('ReleaseRaw', foreign_keys=[release_id], innerjoin=True)


class CountryArea(Base):
    __tablename__ = 'country_area'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='country_area_fk_area'), primary_key=True)

    area = relationship('Area', foreign_keys=[area_id])


class DeletedEntity(Base):
    __tablename__ = 'deleted_entity'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    gid = Column(UUID, nullable=False, primary_key=True)
    data = Column(JSONB, nullable=False)
    deleted_at = Column(DateTime(timezone=True), nullable=False, server_default=sql.func.now())


class Edit(Base):
    __tablename__ = 'edit'
    __table_args__ = (
        Index('edit_idx_type_id', 'type', 'id'),
        Index('edit_idx_open_time', 'open_time'),
        Index('edit_idx_close_time', 'close_time'),
        Index('edit_idx_expire_time', 'expire_time'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='edit_fk_editor'), nullable=False)
    type = Column(SMALLINT, nullable=False)
    status = Column(SMALLINT, nullable=False)
    autoedit = Column(SMALLINT, nullable=False, default=0, server_default=sql.text('0'))
    open_time = Column(DateTime(timezone=True), server_default=sql.func.now())
    close_time = Column(DateTime(timezone=True))
    expire_time = Column(DateTime(timezone=True), nullable=False)
    language_id = Column('language', Integer, ForeignKey(apply_schema('language.id', 'musicbrainz'), name='edit_fk_language'))
    quality = Column(SMALLINT, nullable=False, default=1, server_default=sql.text('1'))

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    language = relationship('Language', foreign_keys=[language_id])


class EditData(Base):
    __tablename__ = 'edit_data'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_data_fk_edit'), nullable=False, primary_key=True)
    data = Column(JSONB, nullable=False)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)


class EditNote(Base):
    __tablename__ = 'edit_note'
    __table_args__ = (
        Index('edit_note_idx_edit', 'edit'),
        Index('edit_note_idx_editor', 'editor'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='edit_note_fk_editor'), nullable=False)
    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_note_fk_edit'), nullable=False)
    text = Column(String, nullable=False)
    post_time = Column(DateTime(timezone=True), server_default=sql.func.now())

    editor = relationship('Editor', foreign_keys=[editor_id], innerjoin=True)
    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)


class EditNoteRecipient(Base):
    __tablename__ = 'edit_note_recipient'
    __table_args__ = (
        Index('edit_note_recipient_idx_recipient', 'recipient'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    recipient_id = Column('recipient', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='edit_note_recipient_fk_recipient'), nullable=False, primary_key=True)
    edit_note_id = Column('edit_note', Integer, ForeignKey(apply_schema('edit_note.id', 'musicbrainz'), name='edit_note_recipient_fk_edit_note'), nullable=False, primary_key=True)

    recipient = relationship('Editor', foreign_keys=[recipient_id], innerjoin=True)
    edit_note = relationship('EditNote', foreign_keys=[edit_note_id], innerjoin=True)


class EditArea(Base):
    __tablename__ = 'edit_area'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_area_fk_edit'), nullable=False, primary_key=True)
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='edit_area_fk_area', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    area = relationship('Area', foreign_keys=[area_id], innerjoin=True)


class EditArtist(Base):
    __tablename__ = 'edit_artist'
    __table_args__ = (
        Index('edit_artist_idx', 'artist'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_artist_fk_edit'), nullable=False, primary_key=True)
    artist_id = Column('artist', Integer, ForeignKey(apply_schema('artist.id', 'musicbrainz'), name='edit_artist_fk_artist', ondelete='CASCADE'), nullable=False, primary_key=True)
    status = Column(SMALLINT, nullable=False)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    artist = relationship('Artist', foreign_keys=[artist_id], innerjoin=True)


class EditEvent(Base):
    __tablename__ = 'edit_event'
    __table_args__ = (
        Index('edit_event_idx', 'event'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_event_fk_edit'), nullable=False, primary_key=True)
    event_id = Column('event', Integer, ForeignKey(apply_schema('event.id', 'musicbrainz'), name='edit_event_fk_event', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    event = relationship('Event', foreign_keys=[event_id], innerjoin=True)


class EditGenre(Base):
    __tablename__ = 'edit_genre'
    __table_args__ = (
        Index('edit_genre_idx', 'genre'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_genre_fk_edit'), nullable=False, primary_key=True)
    genre_id = Column('genre', Integer, ForeignKey(apply_schema('genre.id', 'musicbrainz'), name='edit_genre_fk_genre', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    genre = relationship('Genre', foreign_keys=[genre_id], innerjoin=True)


class EditInstrument(Base):
    __tablename__ = 'edit_instrument'
    __table_args__ = (
        Index('edit_instrument_idx', 'instrument'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_instrument_fk_edit'), nullable=False, primary_key=True)
    instrument_id = Column('instrument', Integer, ForeignKey(apply_schema('instrument.id', 'musicbrainz'), name='edit_instrument_fk_instrument', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    instrument = relationship('Instrument', foreign_keys=[instrument_id], innerjoin=True)


class EditLabel(Base):
    __tablename__ = 'edit_label'
    __table_args__ = (
        Index('edit_label_idx_status', 'status'),
        Index('edit_label_idx', 'label'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_label_fk_edit'), nullable=False, primary_key=True)
    label_id = Column('label', Integer, ForeignKey(apply_schema('label.id', 'musicbrainz'), name='edit_label_fk_label', ondelete='CASCADE'), nullable=False, primary_key=True)
    status = Column(SMALLINT, nullable=False)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    label = relationship('Label', foreign_keys=[label_id], innerjoin=True)


class EditMood(Base):
    __tablename__ = 'edit_mood'
    __table_args__ = (
        Index('edit_mood_idx', 'mood'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_mood_fk_edit'), nullable=False, primary_key=True)
    mood_id = Column('mood', Integer, ForeignKey(apply_schema('mood.id', 'musicbrainz'), name='edit_mood_fk_mood', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    mood = relationship('Mood', foreign_keys=[mood_id], innerjoin=True)


class EditPlace(Base):
    __tablename__ = 'edit_place'
    __table_args__ = (
        Index('edit_place_idx', 'place'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_place_fk_edit'), nullable=False, primary_key=True)
    place_id = Column('place', Integer, ForeignKey(apply_schema('place.id', 'musicbrainz'), name='edit_place_fk_place', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    place = relationship('Place', foreign_keys=[place_id], innerjoin=True)


class EditRelease(Base):
    __tablename__ = 'edit_release'
    __table_args__ = (
        Index('edit_release_idx', 'release'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_release_fk_edit'), nullable=False, primary_key=True)
    release_id = Column('release', Integer, ForeignKey(apply_schema('release.id', 'musicbrainz'), name='edit_release_fk_release', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    release = relationship('Release', foreign_keys=[release_id], innerjoin=True)


class EditReleaseGroup(Base):
    __tablename__ = 'edit_release_group'
    __table_args__ = (
        Index('edit_release_group_idx', 'release_group'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_release_group_fk_edit'), nullable=False, primary_key=True)
    release_group_id = Column('release_group', Integer, ForeignKey(apply_schema('release_group.id', 'musicbrainz'), name='edit_release_group_fk_release_group', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    release_group = relationship('ReleaseGroup', foreign_keys=[release_group_id], innerjoin=True)


class EditRecording(Base):
    __tablename__ = 'edit_recording'
    __table_args__ = (
        Index('edit_recording_idx', 'recording'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_recording_fk_edit'), nullable=False, primary_key=True)
    recording_id = Column('recording', Integer, ForeignKey(apply_schema('recording.id', 'musicbrainz'), name='edit_recording_fk_recording', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    recording = relationship('Recording', foreign_keys=[recording_id], innerjoin=True)


class EditSeries(Base):
    __tablename__ = 'edit_series'
    __table_args__ = (
        Index('edit_series_idx', 'series'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_series_fk_edit'), nullable=False, primary_key=True)
    series_id = Column('series', Integer, ForeignKey(apply_schema('series.id', 'musicbrainz'), name='edit_series_fk_series', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    series = relationship('Series', foreign_keys=[series_id], innerjoin=True)


class EditWork(Base):
    __tablename__ = 'edit_work'
    __table_args__ = (
        Index('edit_work_idx', 'work'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_work_fk_edit'), nullable=False, primary_key=True)
    work_id = Column('work', Integer, ForeignKey(apply_schema('work.id', 'musicbrainz'), name='edit_work_fk_work', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    work = relationship('Work', foreign_keys=[work_id], innerjoin=True)


class EditURL(Base):
    __tablename__ = 'edit_url'
    __table_args__ = (
        Index('edit_url_idx', 'url'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    edit_id = Column('edit', Integer, ForeignKey(apply_schema('edit.id', 'musicbrainz'), name='edit_url_fk_edit'), nullable=False, primary_key=True)
    url_id = Column('url', Integer, ForeignKey(apply_schema('url.id', 'musicbrainz'), name='edit_url_fk_url', ondelete='CASCADE'), nullable=False, primary_key=True)

    edit = relationship('Edit', foreign_keys=[edit_id], innerjoin=True)
    url = relationship('URL', foreign_keys=[url_id], innerjoin=True)


class Editor(Base):
    __tablename__ = 'editor'
    __table_args__ = (
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False)
    privs = Column(Integer, default=0, server_default=sql.text('0'))
    email = Column(String(64))
    website = Column(String(255))
    bio = Column(String)
    member_since = Column(DateTime(timezone=True), server_default=sql.func.now())
    email_confirm_date = Column(DateTime(timezone=True))
    last_login_date = Column(DateTime(timezone=True), server_default=sql.func.now())
    last_updated = Column(DateTime(timezone=True), server_default=sql.func.now())
    birth_date = Column(Date)
    gender_id = Column('gender', Integer, ForeignKey(apply_schema('gender.id', 'musicbrainz'), name='editor_fk_gender'))
    area_id = Column('area', Integer, ForeignKey(apply_schema('area.id', 'musicbrainz'), name='editor_fk_area'))
    password = Column(String(128), nullable=False)
    ha1 = Column(CHAR(32), nullable=False)
    deleted = Column(Boolean, nullable=False, default=False, server_default=sql.false())

    gender = relationship('Gender', foreign_keys=[gender_id])
    area = relationship('Area', foreign_keys=[area_id])


class EditorLanguage(Base):
    __tablename__ = 'editor_language'
    __table_args__ = (
        Index('editor_language_idx_language', 'language'),
        {'schema': mbdata.config.schemas.get('musicbrainz', 'musicbrainz')}
    )

    editor_id = Column('editor', Integer, ForeignKey(apply_schema('editor.id', 'musicbrainz'), name='editor_language_fk_editor'), nullable=False, primary_key=True)
    language_id = Column('language', Integer, ForeignKey(apply_schema('language.id', 'musicbrainz'), name='editor_language_fk_language'), nullable=False, primary_key=True)
