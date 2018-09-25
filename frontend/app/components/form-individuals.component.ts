import { Component, OnInit } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';


@Component({
  selector: "pnx-cmr-individuals",
  templateUrl: "form_individuals.component.html"
})
export class IndividualsComponent implements OnInit {
  public individuals: Array<any>;
  constructor(private _api: HttpClient) { }

  ngOnInit() {
    this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/individuals`)
      .subscribe(data => {
        this.individuals = data;
        console.log(data);
      })

  }
}
