import { Component, OnInit } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';
import { MapService } from "@geonature_common/map/map.service";
import { ActivatedRoute } from "@angular/router";


@Component({
  selector: "pnx-cmr-sites",
  templateUrl: "sites.component.html"
})
export class SitesComponent implements OnInit {
  public sites: Array<any>;
  constructor(private _api: HttpClient, private route: ActivatedRoute) {

  }

  ngOnInit() {
    this.route.params.subscribe(params => {
      console.log(params);
      this._api.get<any>(`${AppConfig.API_ENDPOINT}/cmr/sites/` + params.id_program)
        .subscribe(data => {
          this.sites = data.features;
          console.log(data);
        })
    })

  }
}
