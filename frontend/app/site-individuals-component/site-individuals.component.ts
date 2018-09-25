import { Component, OnInit } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';

import { Router, ActivatedRoute } from '@angular/router';
@Component({
  selector: "pnx-cmr-site-individuals",
  templateUrl: "site-individuals.component.html",
  styleUrls: ['site-individuals.component.scss']

})
export class SiteIndividualsComponent implements OnInit {
  public individuals : Array<any>;
  constructor(private _api: HttpClient, private _router: Router, private _actRoute: ActivatedRoute) {
  
  }

  ngOnInit() {
    this._actRoute.params.subscribe(params => {
      this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/sites/${params.id_site}/individuals`)
        .subscribe(data => {
          this.individuals = data;
        })
    })
  }

  onInfo() {
    this._router.navigate([`cmr/operations`]);
  }
}
