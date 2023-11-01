

To list recent packages:

.. code:: bash

    python -m watch.mlops.manager "list packages" --dataset_codes Drop7-Cropped2GSD


.. code:: bash

    HIRES_DVC_DATA_DPATH=$(geowatch_dvc --tags='drop7_data' --hardware=auto)
    TRUTH_DVC_DATA_DPATH=$(geowatch_dvc --tags='phase2_data' --hardware=auto)
    DVC_EXPT_DPATH=$(geowatch_dvc --tags='phase2_expt' --hardware=auto)
    BUNDLE_DPATH=$HIRES_DVC_DATA_DPATH/Drop7-Cropped2GSD-V2

    kwcoco stats \
        --io_workers=8 \
        $BUNDLE_DPATH/KR_R001/imgonly-KR_R001-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/KR_R002/imgonly-KR_R002-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/CH_R001/imgonly-CH_R001-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/KW_C001/imgonly-KW_C001-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/CO_C001/imgonly-CO_C001-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/CN_C000/imgonly-CN_C000-rawbands.kwcoco.zip

    geowatch stats \
        --io_workers=8 \
        $BUNDLE_DPATH/KR_R001/imgonly-KR_R001-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/KR_R002/imgonly-KR_R002-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/CH_R001/imgonly-CH_R001-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/KW_C001/imgonly-KW_C001-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/CO_C001/imgonly-CO_C001-rawbands.kwcoco.zip \
        $BUNDLE_DPATH/CN_C000/imgonly-CN_C000-rawbands.kwcoco.zip

    # $BUNDLE_DPATH/SA_C001/imgonly-SA_C001-rawbands.kwcoco.zip
    # $BUNDLE_DPATH/VN_C002/imgonly-VN_C002-rawbands.kwcoco.zip

    HIRES_DVC_DATA_DPATH=$(geowatch_dvc --tags='drop7_data' --hardware=auto)
    TRUTH_DVC_DATA_DPATH=$(geowatch_dvc --tags='phase2_data' --hardware=auto)
    DVC_EXPT_DPATH=$(geowatch_dvc --tags='phase2_expt' --hardware=auto)
    BUNDLE_DPATH=$HIRES_DVC_DATA_DPATH/Drop7-Cropped2GSD-V2
    python -m watch.mlops.schedule_evaluation --params="
        pipeline: sc

        matrix:
            ########################
            ## AC/SC PIXEL PARAMS ##
            ########################

            sc_pxl.test_dataset:
                #- $BUNDLE_DPATH/KR_R001/imgonly-KR_R001-rawbands.kwcoco.zip
                - $BUNDLE_DPATH/KR_R002/imgonly-KR_R002-rawbands.kwcoco.zip
                - $BUNDLE_DPATH/KW_C001/imgonly-KW_C001-rawbands.kwcoco.zip
                #- $BUNDLE_DPATH/CO_C001/imgonly-CO_C001-rawbands.kwcoco.zip
                #- $BUNDLE_DPATH/CN_C000/imgonly-CN_C000-rawbands.kwcoco.zip

            sc_pxl.package_fpath:
                - $DVC_EXPT_DPATH/models/fusion/Drop4-SC/packages/Drop4_tune_V30_8GSD_V3/Drop4_tune_V30_8GSD_V3_epoch=2-step=17334.pt.pt
                - $DVC_EXPT_DPATH/models/fusion/Drop7-Cropped2GSD/packages/Drop7-Cropped2GSD_SC_bgrn_gnt_sgd_split6_V86/Drop7-Cropped2GSD_SC_bgrn_gnt_sgd_split6_V86_epoch=189-step=12160-val_loss=2.881.pt
                #- $DVC_EXPT_DPATH/models/fusion/Drop7-Cropped2GSD/packages/Drop7-Cropped2GSD_SC_bgrn_split6_V07/Drop7-Cropped2GSD_SC_bgrn_split6_V07_epoch73_step6364.pt
                #- $DVC_EXPT_DPATH/models/fusion/Drop7-Cropped2GSD/packages/Drop7-Cropped2GSD_SC_bgrn_split6_V11/Drop7-Cropped2GSD_SC_bgrn_split6_V11_epoch444_step19135.pt

            sc_pxl.tta_fliprot: 0.0
            sc_pxl.tta_time: 0.0
            sc_pxl.chip_overlap: 0.3

            ## Typically leave these as 'auto', but
            ## you can overwrite them if desired.
            #sc_pxl.input_space_scale: 2GSD
            #sc_pxl.window_space_scale: 2GSD
            #sc_pxl.output_space_scale: 2GSD
            #sc_pxl.time_span: 6m
            #sc_pxl.time_sampling: auto
            #sc_pxl.time_steps: 12
            #sc_pxl.chip_dims: auto

            sc_pxl.fixed_resolution:
                - null
                - 2GSD
                - 8GSD

            sc_pxl.set_cover_algo: null
            sc_pxl.resample_invalid_frames: 3
            sc_pxl.observable_threshold: 0.0
            sc_pxl.mask_low_quality: true
            sc_pxl.drop_unused_frames: true
            sc_pxl.num_workers: 12
            sc_pxl.batch_size: 1
            sc_pxl.write_workers: 0

            ########################
            ## AC/SC POLY PARAMS  ##
            ########################

            sc_poly.thresh:
             - 0.07
             - 0.10
             - 0.20
             - 0.30
            sc_poly.boundaries_as: polys
            #sc_poly.resolution: 2GSD
            sc_poly.min_area_square_meters: 7200

            #############################
            ## AC/SC POLY EVAL PARAMS  ##
            #############################

            sc_poly_eval.true_site_dpath: $TRUTH_DVC_DATA_DPATH/annotations/drop7-hard-v1/site_models
            sc_poly_eval.true_region_dpath: $TRUTH_DVC_DATA_DPATH/annotations/drop7-hard-v1/region_models

            ##################################
            ## HIGH LEVEL PIPELINE CONTROLS ##
            ##################################
            sc_pxl.enabled: 1
            sc_pxl_eval.enabled: 0
            sc_poly.enabled: 1
            sc_poly_eval.enabled: 1
            sc_poly_viz.enabled: 0

        submatrices:

            # Might abstract this for convinience later.

            - sc_pxl.test_dataset: $BUNDLE_DPATH/KR_R001/imgonly-KR_R001-rawbands.kwcoco.zip
              sc_poly.site_summary: $TRUTH_DVC_DATA_DPATH/annotations/drop7-hard-v1/region_models/KR_R001.geojson

            - sc_pxl.test_dataset: $BUNDLE_DPATH/KR_R002/imgonly-KR_R002-rawbands.kwcoco.zip
              sc_poly.site_summary: $TRUTH_DVC_DATA_DPATH/annotations/drop7-hard-v1/region_models/KR_R002.geojson

            - sc_pxl.test_dataset: $BUNDLE_DPATH/CH_R001/imgonly-CH_R001-rawbands.kwcoco.zip
              sc_poly.site_summary: $TRUTH_DVC_DATA_DPATH/annotations/drop7-hard-v1/region_models/CH_R001.geojson

            - sc_pxl.test_dataset: $BUNDLE_DPATH/KW_C001/imgonly-KW_C001-rawbands.kwcoco.zip
              sc_poly.site_summary: $TRUTH_DVC_DATA_DPATH/annotations/drop7-hard-v1/region_models/KW_C001.geojson

            - sc_pxl.test_dataset: $BUNDLE_DPATH/CO_C001/imgonly-CO_C001-rawbands.kwcoco.zip
              sc_poly.site_summary: $TRUTH_DVC_DATA_DPATH/annotations/drop7-hard-v1/region_models/CO_C001.geojson

            - sc_pxl.test_dataset: $BUNDLE_DPATH/CN_C000/imgonly-CN_C000-rawbands.kwcoco.zip
              sc_poly.site_summary: $TRUTH_DVC_DATA_DPATH/annotations/drop7-hard-v1/region_models/CN_C000.geojson

        " \
        --root_dpath="$DVC_EXPT_DPATH/_ac_baseline" \
        --queue_name "_ac_baseline" \
        --devices="0,1" \
        --backend=tmux --tmux_workers=4 \
        --cache=1 --skip_existing=1 --run=1


To aggregate results

.. code:: bash

    HIRES_DVC_DATA_DPATH=$(geowatch_dvc --tags='drop7_data' --hardware=auto)
    TRUTH_DVC_DATA_DPATH=$(geowatch_dvc --tags='phase2_data' --hardware=auto)
    DVC_EXPT_DPATH=$(geowatch_dvc --tags='phase2_expt' --hardware=auto)
    BUNDLE_DPATH=$HIRES_DVC_DATA_DPATH/Drop7-Cropped2GSD-V2

    python -m watch.mlops.aggregate \
        --pipeline=sc \
        --target "
            - $DVC_EXPT_DPATH/_ac_baseline
        " \
        --output_dpath="$DVC_EXPT_DPATH/_ac_baseline/aggregate" \
        --resource_report=0 \
        --eval_nodes="
            - sc_poly_eval
        " \
        --plot_params="
            enabled: 0
            stats_ranking: 0
            min_variations: 1
            params_of_interest:
                - params.sc_poly.thresh
        " \
        --stdout_report="
            top_k: 100
            per_group: 1
            macro_analysis: 0
            analyze: 0
            print_models: True
            reference_region: final
            concise: 1
            show_csv: 0
        " \
        --rois="KR_R002"
        #--rois="KR_R002,KW_C001"

        #--rois="KR_R002,CN_C000,KW_C001,CO_C001"


python -m watch.tasks.fusion.predict \
    --package_fpath=/home/joncrall/remote/toothbrush/data/dvc-repos/smart_expt_dvc/models/fusion/Drop7-Cropped2GSD/packages/Drop7-Cropped2GSD_SC_bgrn_gnt_sgd_split6_V86/Drop7-Cropped2GSD_SC_bgrn_gnt_sgd_split6_V86_epoch=189-step=12160-val_loss=2.881.pt \
    --test_dataset=/media/joncrall/flash1/smart_drop7/Drop7-Cropped2GSD-V2/KR_R002/imgonly-KR_R002-rawbands.kwcoco.zip \
    --pred_dataset=/home/joncrall/remote/toothbrush/data/dvc-repos/smart_expt_dvc/_ac_baseline/pred/flat/sc_pxl/sc_pxl_id_3cfcc51a/pred.kwcoco.zip \
    --tta_fliprot=0.0 \
    --tta_time=0.0 \
    --chip_overlap=0.3 \
    --fixed_resolution=8GSD \
    --set_cover_algo=None \
    --resample_invalid_frames=3 \
    --observable_threshold=0.0 \
    --mask_low_quality=True \
    --drop_unused_frames=True \
    --write_workers=0 \
    --with_saliency=True \
    --with_class=True \
    --with_change=False \
    --saliency_chan_code=ac_salient  \
    --num_workers=12 \
    --batch_size=1 \
    --devices=0,

python -m watch.tasks.fusion.predict --package_fpath=/home/joncrall/remote/toothbrush/data/dvc-repos/smart_expt_dvc/models/fusion/Drop4-SC/packages/Drop4_tune_V30_8GSD_V3/Drop4_tune_V30_8GSD_V3_epoch=2-step=17334.pt.pt --test_dataset=/media/joncrall/flash1/smart_drop7/Drop7-Cropped2GSD-V2/KR_R001/imgonly-KR_R001-rawbands.kwcoco.zip --pred_dataset=/home/joncrall/remote/toothbrush/data/dvc-repos/smart_expt_dvc/_ac_baseline/pred/flat/sc_pxl/sc_pxl_id_713513e5/pred.kwcoco.zip --tta_fliprot=0.0 --tta_time=0.0 --chip_overlap=0.3 --fixed_resolution=auto --set_cover_algo=None --resample_invalid_frames=3 --observable_threshold=0.0 --mask_low_quality=True --drop_unused_frames=True --write_workers=0 --with_saliency=True --with_class=True --with_change=False --saliency_chan_code=ac_salient --num_workers=12 --batch_size=1 --devices=0,
