import { FormControl, FormGroup, FormBuilder, Validators} from '@angular/forms';
import { Component, OnInit } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';
import { NomenclatureComponent } from '@geonature_common/form/nomenclature/nomenclature.component';
import { NomenclatureDisplayComponent } from "./utils/nomenclature_display.component";

@Component({
  selector: "pnx-cmr-operations",
  templateUrl: "operations.component.html"
})
export class OperationsComponent implements OnInit {
  public operations: Array<any>;
  public operationsForm: FormGroup;
  constructor(private _api: HttpClient, private formbuilder: FormBuilder) { }

  ngOnInit() {

    this.operationsForm = this.formbuilder.group(
      {'id_nomenclature_cmr_action': [ null, Validators.required],
      'id_nomenclature_obs_method': [ null, Validators.required],
      'id_nomenclature_life_stage': [ null, Validators.required],
      'id_nomenclature_bio_condition': [ null, Validators.required],
      'id_nomenclature_determination_method': [ null, Validators.required]

    },

    );

    this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/operations`)
    .subscribe(data => {

      console.log("data");
      this.operations = data.features;

      })

  }
}
