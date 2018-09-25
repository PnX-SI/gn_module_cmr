import { FormControl, FormGroup, FormBuilder, Validators} from '@angular/forms';
import { Component, OnInit } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';
import { NomenclatureComponent } from '@geonature_common/form/nomenclature/nomenclature.component';
import { NomenclatureDisplayComponent } from "./utils/nomenclature_display.component";
import { Router, ActivatedRoute } from "@angular/router";
import { CommonService} from "@geonature_common/service/common.service";
import { NgbDateParserFormatter } from "@ng-bootstrap/ng-bootstrap";


@Component({
  selector: "pnx-cmr-operations",
  templateUrl: "operations.component.html"
})
export class OperationsComponent implements OnInit {

  public operations: Array<any>;
  public operationsForm: FormGroup;

  constructor(
    private _api: HttpClient,
    private _formbuilder: FormBuilder,
    private _route: ActivatedRoute,
    private _router: Router,
    private _commonService: CommonService,
    private _dateParser: NgbDateParserFormatter,
    ) { };

  ngOnInit() {

    this.operationsForm = this._formbuilder.group({

      'id_nomenclature_cmr_action': [ null, Validators.required],
      'id_nomenclature_obs_method': [ null, Validators.required],
      'id_nomenclature_life_stage': [ null, Validators.required],
      'id_nomenclature_bio_condition': [ null, Validators.required],
      'id_nomenclature_determination_method': [ null, Validators.required],
      'id_individual' : [null, Validators.required],
      'id_site' : [null, Validators.required],
      'id_operation' : [null],
      'date_min': [null],
      'date_max': [null],
      'geom_point_4326': [null],

    });

    this._route.params.subscribe(params => {

      console.log(params);

      this._api.get<any>(AppConfig.API_ENDPOINT + '/cmr/site/' + params.id_site + '/individual/' + params.id_indiv + '/operations')
      .subscribe(data => {

        this.operations = data.features;
        this.operationsForm.patchValue({
          "id_individual": params.id_indiv,
          "id_site": params.id_site,
          "id_nomenclature_cmr_action": 476,
          "id_nomenclature_obs_method": 61,
          "id_nomenclature_life_stage": 18,
          "id_nomenclature_bio_condition": 157,
          "id_nomenclature_determination_method": 344});
      });

    });

  }

  postOp() {

    const op = Object.assign({}, this.operationsForm.value);

    let return_url = AppConfig.API_ENDPOINT + '/cmr/site/' + op.id_site + '/individual/' + op.id_indiv + '/operations';

    let post_url = AppConfig.API_ENDPOINT + '/cmr/operations';

    // op.date_min = new Date("2016-01-16T16:00:00");
    // op.date_max = new Date("2016-01-16T16:00:00");
    op.date_max = this._dateParser.format(op.date_max);
    op.date_min = this._dateParser.format(op.date_min);

    if(op.id_operation) {

      console.log("Update TODO");
      return;

    }

    this._api.post<any>( `${post_url}`, op).subscribe(

      data => {
        this._router.navigate(return_url);
        this._commonService.translateToaster('success', 'Operation ajoutée avec succès');
      },
      error => {
        this._commonService.translateToaster('error', 'Error');
      }

      );

  };

  setGeom(event) {

    this.operationsForm.patchValue({'geom_point_4326': event});

  };

}
