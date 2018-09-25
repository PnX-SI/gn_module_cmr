import { Component, OnInit } from "@angular/core";
import { HttpClient } from '@angular/common/http';
import { AppConfig } from '@geonature_config/app.config';
import { MapService } from "@geonature_common/map/map.service";
import { ActivatedRoute } from "@angular/router";
import { MapListService } from '@geonature_common/map-list/map-list.service';


@Component({
  selector: "pnx-cmr-sites",
  templateUrl: "sites.component.html",
  styleUrls: ["sites.component.css"]
})
export class SitesComponent implements OnInit {
  public sites: Array<any>;
  public id_site;
  constructor(
    private _api: HttpClient,
    private route: ActivatedRoute,
    public mapListService: MapListService
  ) {

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

    this.mapListService.onMapClik$.subscribe(id => {
      console.log(id);
      this.id_site = id;
    });

  }

  onEachFeature(feature, layer) {
    // event from the map
    this.mapListService.layerDict[feature.id] = layer;
    layer.on({
      click: e => {
        // toggle style
        this.mapListService.toggleStyle(layer);
        // observable
        this.mapListService.mapSelected.next(feature.id);
        // open popup
        // layer.bindPopup(feature.properties.leaflet_popup).openPopup();
      }
    });
  }
}
