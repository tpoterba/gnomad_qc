import hail as hl
from gnomad_qc.v3.resources import get_gnomad_v3_mt, last_END_position

# END RESOURCES

mt = get_gnomad_v3_mt()
mt = mt.select_entries('END')
t = mt._localize_entries('__entries', '__cols')
t = t.select(
    last_END_position=hl.or_else(
        hl.min(
            hl.scan.array_agg(
                lambda entry: hl.scan._prev_nonnull(
                    hl.or_missing(
                        hl.is_defined(entry.END),
                        hl.tuple([
                            t.locus,
                            entry.END
                        ])
                    )
                ),
                t.__entries
            ).map(
                lambda x: hl.or_missing(
                    (x[1] >= t.locus.position) & (x[0].contig == t.locus.contig),
                    x[0].position
                )
            )
        ),
        t.locus.position
    )
)
t.write(last_END_position.path, overwrite=True)

