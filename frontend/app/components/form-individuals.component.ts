import { Component, OnInit } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';


@Component({
  selector: "pnx-cmr-individuals",
  templateUrl: "form_individuals.component.html"
})
export class OperationsComponent implements OnInit {
  public individuals: Array<any>;
  constructor(private _api: HttpClient) { }

  ngOnInit() {
    this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/operations`)
      .subscribe(data => {
        this.operations = data;
        console.log(data);
      })

  }
}
