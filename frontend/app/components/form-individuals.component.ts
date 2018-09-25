import { Component, OnInit } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';
import { IndividualsService } from "../services/individuals.service";


@Component({
  selector: "pnx-cmr-individuals",
  templateUrl: "form-individuals.component.html"
})
export class IndividualsFormComponent implements OnInit {
  public individuals: Array<any>;
  constructor(private _api: IndividualsService) { }

  ngOnInit() {
    console.debug(this._api)
    this._api.getAllIndividuals()
      .subscribe(data => {
        this.individuals = data;
        console.log(data);
      })

  }
}
