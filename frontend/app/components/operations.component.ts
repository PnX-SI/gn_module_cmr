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
      {'id_nomenclature_cmr_action': [ null, Validators.required]},

      );

    this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/operations`)
      .subscribe(data => {
        this.operations = data;
        this.operationsForm.patchValue(this.operations[0])
        console.log(data);
      })


    console.log(this.operationsForm);
  }
}
